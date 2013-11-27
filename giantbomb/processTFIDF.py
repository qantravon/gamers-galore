#process tf-idf for every game description
#	~20k games
#	~246k terms

import re
import os
import xml.etree.ElementTree as ET
from stemming import porter2
import math


############################GLOBAL VARS########################################
IDS = []
TOKENS = []
IDF = []
###############################################################################


#	CLASS FOR HANDLING TF-IDF CALCULATIONS
class InvertedIndex():
	def __init__(self):
		self.inverted_index={}		#listed game ID for one appearence of the token

	def __del__(self):
		del self.inverted_index
		
	def index_terms(self, id, tokens):
		IDS.append(id)
		for token in tokens:
			if token not in self.inverted_index:
				self.inverted_index[token] = []
				TOKENS.append(token)
			self.inverted_index[token].append(id)

	def calc_idf(self):
		df = []
		for token in self.inverted_index:
			df.append(len(set(self.inverted_index[token])))
		for num in df:
			IDF.append(math.log((len(IDS)/num), 2))

	def printResults(self):
		with open("invertedIndex.txt",'w') as file:
			for token in self.inverted_index:
				file.write(token + ' :')
				for val in self.inverted_index[token]:
					file.write(' ' + val)
				file.write('\n')

##################################GLOBAL VAR####################################

stats = InvertedIndex()

################################################################################



#		GLOBAL FUNCTIONS		#

def tokenize(text):
	tokens = re.findall("[\w']+", text.lower())
	return [porter2.stem(token) for token in tokens]

def processDescription(id, desc):
	if desc != '':
		tokens = tokenize(desc)
		stats.index_terms(id, tokens)

def openFiles():
	with open("IDs.txt", 'r') as file:
		for line in file:
			id = (line.split())[0]
			root = ET.parse('games/'+id+'.xml').getroot()
			if root[2].text != None:
				processDescription(id, root[2].text.encode('utf-8'))

def calc_TF(id):
	print id
	vals=[]
	with open("invertedIndex.txt",'r') as file:
		for line in file:
			numID = (line.split(':'))[1].split()
			vals.append(numID.count(id))
	print vals
	return vals

def calc_TFIDF(termfreq):
	i=0
	for num in termfreq:
		termfreq[i] = num * IDF[i]
		i=i+1
	return termfreq

#		END GLOBAL FUNCTIONS		#
		



###############################################################################
#							MAIN CODE										  #
###############################################################################
def main():
	global stats
	print 'indexing...'
	openFiles()
	print 'calculating IDF...'
	stats.calc_idf()
	print IDF
	print 'printing inverted index to file...'
	stats.printResults()
	print 'deleting index...'
	del stats
	print 'DONE!\n'

	print 'calculating TF.IDF scores now...'
	for id in IDS:
		_termFreq = calc_TFIDF(calc_TF(id))
		with open("scores/"+str(id)+".txt",'w') as file:
			for num in _termFreq:
				file.write('%f ' % num)
	
if __name__ == '__main__':
	main()
	