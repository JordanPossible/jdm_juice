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
	# // les types de noeuds (Nodes Types) : nt;ntid;'ntname'
	nodes_types = []
	# // les types de relations (Relation Types) : rt;rtid;'trname';'trgpname';'rthelp'
	rels_types = []
	# // les noeuds/termes (Entries) : e;eid;'name';type;w;'formated name'
	noeuds = []
	# // les relations sortantes : r;rid;node1;node2;type;w
	relations_sortantes = []
	# // les relations entrantes : r;rid;node1;node2;type;w
	relations_entrantes = []

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
			# We add a dico to the nodes_types list
			# where the key is the ntid (eg: node type id) and the value is the ntname (eg: node type name)
			node_type_dico = {}
			node_type_splited = line.split(";")
			node_type_dico[node_type_splited[1]] = [node_type_splited[2]]
			nodes_types.append(node_type_dico)
		if line.startswith("e;"):
			# print("E")
			noeuds.append(line)
		if line.startswith("rt;"):
			# print("RT")
			rels_types.append(line)
		if line.startswith("r;") and relation_sortantes:
			# print("R_S")
			relations_sortantes.append(line)
		if line.startswith("r;") and not relation_sortantes:
			# print("R_E")
			relations_entrantes.append(line)
		if line.startswith(" "):
			print("DEF_EXEMPLE")
		if line:
			if line[0].isdigit():
				print("DEF")
		if line.startswith("// les relations entrantes"):
			relation_sortantes = False

	# We start building a dict object from our data
	data = {}
	data['title'] = word_query

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
