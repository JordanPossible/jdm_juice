#!flask/bin/python
from flask import Flask
from flask_cors import CORS
import urllib2
from bs4 import BeautifulSoup
from lxml import html
import time

app = Flask(__name__)
CORS(app)

# Retourne le html du rezo-dump jdm
def get_rezo_dump(query):
	# l'url du reseau dump est concat avec la query
	url = "http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel=" + query + "&rel="
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	# dump_str correspond au html contenu dans les balise <CODE>
	dump_str = str(soup.find_all('code'))
	return dump_str

# Formate le html pour renvoyer une belle structure
def prepare_json(dump_str):
	# the JSON result
	data = {}
	soup = BeautifulSoup(dump_str, 'html.parser')
	# Prepare le block definition
	def_block =  str(soup.find_all('def'))
	# On veut split sur les "<br>" et "<br/>" alors on remplace pour avoir a faire un seul split
	def_block = def_block.replace("<br>", "<br/>")
	splited = def_block.split("<br/>")

	indice_def = 0
	indice_exemple = 0
	for elem in splited:
		# Si on a un "n" en troisieme position de la string alors c'est une definition
		if(elem.startswith("n", 2, 3)):
			indice_exemple = 0
			print "DEF" + str(indice_def)
			indice_def+=1
			print elem + "\n"
		# Sinon si le n est en quatrieme poisiton alors c'est un exemple donne a la definition precedente
		elif(elem.startswith("n", 3, 4)):
			print "EXEMPLE" + str(indice_exemple)
			indice_exemple += 1
			print elem + "\n"

	return def_block




# Recupere le contenu du rezo-dump, le prepare avec soin et retourne a angular
@app.route('/mots/<word_query>', methods=['GET'])
def render_content(word_query):
	# demare un timer
	t_start = time.time()
	# get le html et le prepare
	dump_str = get_rezo_dump(word_query)
	result = prepare_json(dump_str)
	# stop le timer et print le temps d'execution
	t_end = time.time()
	print("TIMER : " + str(t_end - t_start))
	return result


if __name__ == '__main__':
    app.run(debug=True)
