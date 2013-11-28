import xml.etree.ElementTree as ET
import datetime
import urllib2
import math
import requests
from HTMLParser import HTMLParser
import re
from xml.dom.minidom import parseString


steamWAPI = 'http://api.steampowered.com/'
steamKEY = ''

giantBombWAPI = 'http://www.giantbomb.com/api/'
giantBombKEY = ''
#giantBombKEY = ''
#giantBombKEY = ''

gamesRadarWAPI = 'http://api.gamesradar.com/'
gamesRadarKEY = ''
gamesRadarSECRET = ''

#http://steamcommunity.com/profiles/76561197979836184

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed=[]
	def handle_data(self,d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def striphtml(data):
	if data.isspace():
		return ''
	s=MLStripper()
	s.feed(data)
	return s.get_data()

def steamTest():
	STEAM_USERNAME = 'qantravon'
	username_r = requests.get('http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(STEAM_USERNAME))
	steamid = str(parseString(username_r.text.encode('utf-8')).getElementsByTagName('steamID64')[0].firstChild.wholeText)
	playerStats = urllib2.urlopen(steamWAPI+'ISteamUser/GetPlayerSummaries/v0002/?key='+steamKEY+'&steamids='+steamid+'&format=xml')

def extractGameInfo(_info):
	info = {}
	info['description'] = ''
	if _info[0].text != None:			#check to see if field is null before parsing
		info['description'] = striphtml(_info[0].text)
	info['genres'] = []
	info['similarGames'] = []
	
	temp = _info.find('genres')
	if temp != None:					#check to see if field is null
		for genre in temp:
			info['genres'].append((genre[1].text,genre[2].text))
	temp = _info.find('similar_games')
	if temp != None:					#check to see if field is null
		for similarGame in temp:
			info['similarGames'].append((similarGame[1].text,similarGame[2].text))
	return info
		
def giantBombTest():
	#40k pc games on GB database (?)
	#0-100, 100-200, 200-300, 300-400
	
	for i in range(375,405):
		#retrieve list of PC game names and their ID
		_games = requests.get(giantBombWAPI+'games/?api_key=%s&field_list=id,image,name&offset=%s&platforms=94&format=xml' % (giantBombKEY, i*100))
		games = ET.fromstring(_games.text.encode('utf-8')).find('results')
		for game in games:
			#extract game information
			id = game[0].text
			#retrieve information for specific game ID	
			_gameInfo = requests.get(giantBombWAPI+'game/%s/?api_key=%s&field_list=description,genres,similar_games&format=xml' % (id, giantBombKEY))
			gameInfo = extractGameInfo(ET.fromstring(_gameInfo.text.encode('utf-8')).find('results'))
			gameInfo['name'] = game[2].text
			with open("IDs.txt","a") as file:
				file.write(id + ' ' + gameInfo['name'].encode('utf-8')+'\n')
			
			#create XML elements
			root = ET.Element("root")
			_id = ET.SubElement(root, "id")
			_id.text = id
			_name = ET.SubElement(root, "name")
			_name.text = gameInfo['name']
			_desc = ET.SubElement(root, "description")
			_desc.text = gameInfo['description']
			_genres = ET.SubElement(root, "genres")
			for _genre in gameInfo['genres']:
				_gen = ET.SubElement(_genres, "genre")
				_gen.set("id", _genre[0])
				_gen.text = _genre[1]
			_sim_games = ET.SubElement(root, "similar_games")
			for _sim_game in gameInfo['similarGames']:
				_game = ET.SubElement(_sim_games, "game")
				_game.set("id", _sim_game[0])
				_game.text = _sim_game[1]
					
			#Seperate xml file for each game, labeled "g<id>.xml" where <id> is the game ID
			#Store data to xml file in format as follows....
			#---------------------------------------------------------------
			#<?xml version="1.0" encoding="utf-8"?>
			#<root>
			#	<id> id number </id>
			#	<name> name </name>
			#	<description> gameInfo['description'] </description>
			#	<genres>
			#		<genre id = ? /genre>
			#		<genre id = ? /genre>
			#	<similar_games>
			#		<game id = ?> name </game>
			#		<game id = ?> name </game>
			#	<image> link </image>
			#--------------------------------------------------------------
			tree = ET.ElementTree(root)
			f = open("games/g"+id+".xml", "w")						#write to "games" folder
			tree.write(f, encoding='utf-8', xml_declaration=True)
			f.close()

def main():
	#steamTest()
	print "Pulling data..."
	giantBombTest()
	print "DONE!"
	
if __name__ == "__main__":
	main()
	
#end