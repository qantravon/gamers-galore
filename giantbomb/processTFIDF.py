#process tf-idf for every game description
import re
import os
import xml.etree.ElementTree as ET
from stemming import porter2
import math

#	GLOBAL VARS
ids = []

#	CLASS FOR HANDLING TF-IDF CALCULATIONS
class TFIDF():
	def __init__(self):
		self.inverted_index={}		#listed game ID for one appearence of the token
		self.doc_freq=[]
		#self.term_freq={}
		self.TFIDF={}
		
	def index_terms(self, id, tokens):
		for token in tokens:
			if token not in self.inverted_index:
				self.inverted_index[token] = []
			self.inverted_index[token].append(id)
			self.TFIDF[id]=[]
		#print self.TFIDF

	def tf_idf(self, tf, idf):
		# tf is list of frequency for a given token across all docs
		# idf is idf of a given token
		i=0
		for frequency in tf:
			tf[i] = frequency * idf
			i=i+1
		return tf
			
	def termFrequency(self):
		#print self.TFIDF
		tfidf = {}
		#i=0
		#for doc in self.TFIDF:
			#doc = [0] * len(self.inverted_index)
			#for token in self.inverted_index:
				#if token[i] > 0:
					#self.TFIDF[doc][i] = token[i]
			#i=i+1
		for token in self.inverted_index:
			#self.term_freq[token]=[0] * len(self.TFIDF)
			tfidf[token] = [0] * len(self.TFIDF)
		self.doc_freq = [0] * len(self.inverted_index)
		
		i=0
		for token in self.inverted_index:
			y,k= 0,1
			for doc in tf_idf[token]:
				tfidf[token][y]= self.inverted_index[token].count(ids[y])
				if tfidf[token][y] > 0:
					k=k+1
				y=y+1
			self.doc_freq[i] = 1.0+math.log(len(doc_freq)/k, 2)
			tfidf[token] = self.tf_idf(tfidf[token], self.doc_freq[i])
			i=i+1
		return tfidf
		
	def calcDocuments(self, results):
		for doc in self.TFIDF:
			i=0
			doc=[0]*len(self.inverted_index)
			for token in results:
				if doc in token:
					self.TFIDF[doc][i]=self.inverted_index[token].count(doc)
				i=i+1
		

#	GLOBAL VAR FOR CLASS TFIDF
stats = TFIDF()

			
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
		#read = file.readlines(18313)			#100 will be replaced with total number of lines in IDs.txt file
	#for line in head:
			id = (line.split())[0]
			#print id
			#ids.append(id)
			root = ET.parse('games/'+id+'.xml').getroot()
			if root[2].text != None:
				ids.append(id)
				processDescription(id, root[2].text.encode('utf-8'))
				#print 'processing ID:'+ id

		
		
def main():
	print str(0)+'...'
	openFiles()
	print str(1)+'...'
	results = stats.termFrequency()
	print str(2)+'...'
	scores = stats.calcDocuments(results)
	print scores
	#i=0
	#for result in results:
		#if len(results[result]) > 0:
			#file = open('scores/'+ids[i]+'.txt','w')
			#file.write(results[result])
			#file.close()
			#i+=1
		
if __name__ == '__main__':
	main()
	