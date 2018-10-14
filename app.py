#!flask/bin/python
from flask import Flask
from flask_cors import CORS
from flask import jsonify
import urllib2
from bs4 import BeautifulSoup
from lxml import html
import time
import re
import os
import json

app = Flask(__name__)
CORS(app)

# Simply return a list of the file in cache
def load_cache():
	all_files_in_cache = os.listdir("cache/")
	return all_files_in_cache

# Return a file's content from the cache
def cache_out(word_query):
	file_in_cache = open("cache/" + word_query, 'r')
	dump_str = file_in_cache.read()
	file_in_cache.close()
	return dump_str

# Insert a file in the cache
def cache_in(word_query, dump_str):
	new_file_in_cache = open("cache/" + word_query, 'w')
	new_file_in_cache.write(dump_str.encode("utf-8"))
	new_file_in_cache.close()

# Return the dump from jdm rezo-dump
def get_rezo_dump(query):
	# If the query contains multiple words (eg: whitespaces) we need to process it
	# by replacing whitespaces by + so the url will be valid
	if " " in query:
		query = query.replace(" ", "+")
	# We collect the html from this url
	url = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + query + "&rel="
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	# Only the content under <CODE> tags are needed
	dump_str = soup.find('code').getText()
	return dump_str

def cook_json(dump_str, word_query):
	"""// les types de noeuds (Nodes Types) : nt;ntid;'ntname'
	Our nodes_types_dico will be structured as follow :
	For every node_type => 1 entry where :
			The key is the ntid (eg: node type id) and the value is the ntname (eg: node type name)"""
	nodes_types_dico = {}

	"""// les types de relations (Relation Types) : rt;rtid;'trname';'trgpname';'rthelp'
	Our rels_types_dico will be structured as follow :
	For every rel_type => 1 entry where :
			The key is the rtid (eg: relation type id) and the value is the trname (eg: type relation name)"""
	rels_types_dico = {}

	"""// les noeuds/termes (Entries) : e;eid;'name';type;w;'formated name'
	Our nodes_dico will be structured as follow :
	For every nodes => 1 entry where :
		The key is the eid (eg: node id) and the value is a dictionary where :
			The key [name] return the name value
			The key [type] return the type value
			The key [w] return the weight value"""
	nodes_dico = {}

	"""// les relations sortantes : r;rid;node1;node2;type;w
	Our rels_out_dico will be structured as follow :
	For every rels_out => 1 entry where :
		The key is the rid (eg: relation id) and the value is a dictionary where :
			The key [node1] return the node1 value (the node eid)
			The key [node2] return the node2 value (the node eid)
			The key [type] return the relation type value
			The key [w] return the relation weight value"""
	rels_out_dico = {}

	""" // les relations entrantes : r;rid;node1;node2;type;w
	Our rels_in_dico will be structured as follow :
	For every rels_in => 1 entry where :
		The key is the rid (eg: relation id) and the value is a dictionary where :
			The key [node1] return the node1 value (the node eid)
			The key [node2] return the node2 value (the node eid)
			The key [type] return the relation type value
			The key [w] return the relation weight value"""
	rels_in_dico = {}

	definition = []
	definition_ex = []

	# Split all the dump_str on every lines
	splited_dump = dump_str.splitlines()

	"""Every lines should match with a pattern :
	any integers followed by a . (eg: "1.") then it's a definition
	a single whitespace (eg: " ") then it's an example of the previous definition
	nt; (eg: "nt;") then it's a node type
	e; (eg: "e;") then it's a node
	rt; (eg: "rt;") then it's a relation type
	r; (eg: "r;") then it's a relation : we will have to deal with 2 cases (relations sortantes et entrantes)"""
	relation_sortantes = True
	for line in splited_dump:
		if line.startswith("nt;"):
			# We add a new entry in our nodes_types_dico
			# where the key is the ntid (eg: node type id) and the value is the ntname (eg: node type name)
			node_type_splited = line.split(";")
			nodes_types_dico[node_type_splited[1]] = [node_type_splited[2]]

		if line.startswith("rt;"):
			# We add a new entry in our rels_types_dico
			# where the key is the rtid (eg: relation type id) and the value is the trname (eg: type relation name)
			rel_type_splited = line.split(";")
			rels_types_dico[rel_type_splited[1]] = [rel_type_splited[2]]

		if line.startswith("e;"):
			# We create a temporary dictionary where
				# The key [name] return the node name value
				# The key [type] return the node type value
				# The key [w] return the node weight value
			# Then we add a new entry in our nodes_dico
			# Where the key is the eid (eg: node id) and the value is the temporary dictionary
			node_splited = line.split(";")
			tmp_dict = {}
			tmp_dict['name'] = node_splited[2]
			tmp_dict['type'] = node_splited[3]
			tmp_dict['w'] = node_splited[4]
			nodes_dico[node_splited[1]] = tmp_dict

		if line.startswith("r;") and relation_sortantes:
			# We create a temporary dictionary where
				# The key [node1] return the node1 value (the node eid)
				# The key [node2] return the node2 value (the node eid)
				# The key [type] return the relation type value
				# The key [w] return the relation weight value
			# Then we add a new entry in our rels_out_dico
			# Where the key is the rid (eg: relation id) and the value is the temporary dictionary
			rel_splited = line.split(";")
			tmp_dict = {}
			tmp_dict['node1'] = rel_splited[2]
			tmp_dict['node2'] = rel_splited[3]
			tmp_dict['type'] = rel_splited[4]
			# tmp_dict['w'] = node_splited[5]
			rels_out_dico[node_splited[1]] = tmp_dict

		if line.startswith("r;") and not relation_sortantes:
			# We create a temporary dictionary where
				# The key [node1] return the node1 value (the node eid)
				# The key [node2] return the node2 value (the node eid)
				# The key [type] return the relation type value
				# The key [w] return the relation weight value
			# Then we add a new entry in our rels_in_dico
			# Where the key is the rid (eg: relation id) and the value is the temporary dictionary
			rel_splited = line.split(";")
			tmp_dict = {}
			tmp_dict['node1'] = rel_splited[2]
			tmp_dict['node2'] = rel_splited[3]
			tmp_dict['type'] = rel_splited[4]
			# tmp_dict['w'] = node_splited[5]
			rels_in_dico[node_splited[1]] = tmp_dict

		if line.startswith(" "):
		# SALE
			definition_ex.append(line)

		if line:
		# SALE
			if line[0].isdigit():
				definition.append(line)

		if line.startswith("// les relations entrantes"):
			# The relations found will be in for now
			relation_sortantes = False

	# Enhance our nodes_dict by providing a new entry nodes_dico['type_name']
	# which return a string value corresponding to the type's name of the node
	for nodes in nodes_dico:
		nodes_dico[nodes]['type_name'] = nodes_types_dico[nodes_dico[nodes]['type']]
		print(nodes_dico[nodes])
	# Enhance our rels_out_dico by providing a few new entries :
		# rels_out_dico['node1_object'] which return the node1 entry from the nodes_dico
		# rels_out_dico['node2_object'] which return the node2 entry from the nodes_dico
		# rels_out_dico['type_name'] which return a string value corresponding to the type's name of the relation
	for rels in rels_out_dico:
		rels_out_dico[rels]['node1_object'] = nodes_dico[rels_out_dico[rels]['node1']]
		rels_out_dico[rels]['node2_object'] = nodes_dico[rels_out_dico[rels]['node2']]
		rels_out_dico[rels]['type_name'] = rels_types_dico[rels_out_dico[rels]['type']]
	# Enhance our rels_in_dico by providing a few new entries :
		# rels_in_dico['node1_object'] which return the node1 entry from the nodes_dico
		# rels_in_dico['node2_object'] which return the node2 entry from the nodes_dico
		# rels_in_dico['type_name'] which return a string value corresponding to the type's name of the relation
	for rels in rels_in_dico:
		rels_in_dico[rels]['node1_object'] = nodes_dico[rels_in_dico[rels]['node1']]
		rels_in_dico[rels]['node2_object'] = nodes_dico[rels_in_dico[rels]['node2']]
		rels_in_dico[rels]['type_name'] = rels_types_dico[rels_in_dico[rels]['type']]

	# We build a data dict from all our dictionary
	data = {}
	data['title'] = word_query
	data['nodes_types_dico'] = nodes_types_dico
	data['rels_types_dico'] = rels_types_dico
	data['nodes_dico'] = nodes_dico
	data['rels_out_dico'] = rels_out_dico
	data['rels_in_dico'] = rels_in_dico
	data['definition'] = definition
	data['definition_ex'] = definition_ex

	return data

@app.route('/mots/<word_query>', methods=['GET'])
def render_content(word_query):
	# When we query this road, we first want to load the cache
	cache = load_cache()
	# Then we will check the cache to find the query
	if word_query in cache:
			result = cook_json(cache_out(word_query), word_query)
			print("RETURNED FROM THE cache")
			return jsonify(result)

	# If we don't find the query result in the cache, we will find it on the jdm rezo-dump
	else:
		dump_str = get_rezo_dump(word_query)
		cache_in(word_query, dump_str) # We save the dump in our cache
		result = cook_json(dump_str, word_query)
		print("RETURNED FROM THE REZO-DUMP")
		return jsonify(result)


if __name__ == '__main__':
	app.run(debug=True)
