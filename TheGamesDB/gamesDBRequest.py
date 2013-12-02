import xml.etree.ElementTree as ET
import datetime
import urllib2
import math
import requests
from HTMLParser import HTMLParser
import re
from xml.dom.minidom import parseString

gamesDBWAPI = 'http://thegamesdb.net/api/'
gamesDBImgUrl = 'http://thegamesdb.net/banners/'

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

def extractGameInfo(_info):
	info = {}
	info['name'] = ''
	info['overview'] = ''
	info['genres'] = []
	info['platform'] = ''
	info['release_date'] = ''
	info['ESRB'] = ''
	info['co-op'] = ''
	info['publisher'] = ''
	info['developer'] = ''
	info['players'] = ''
	info['rating'] = ''
	info['boxart'] = ''
	
	temp = _info.find('GameTitle')
	if temp != None:
		info['name'] = temp.text
	temp = _info.find('Overview')
	if temp != None:			#check to see if field is null before parsing
		info['overview'] = temp.text
	temp = _info.find('Genres')
	if temp != None:					#check to see if field is null
		for genre in temp:
			info['genres'].append(genre.text)
	temp = _info.find('Platform')
	if temp != None:					#check to see if field is null
		info['platform'] = temp.text
	temp = _info.find('ReleaseDate')
	if temp != None:
		info['release_date'] = temp.text
	temp = _info.find('ESRB')
	if temp != None:
		info['ESRB'] = temp.text
	temp = _info.find('Co-op')
	if temp != None:
		info['co-op'] = temp.text
	temp = _info.find('Publisher')
	if temp != None:
		info['publisher'] = temp.text
	temp = _info.find('Developer')
	if temp != None:
		info['developer'] = temp.text
	temp = _info.find('Players')
	if temp != None:
		info['players'] = temp.text
	temp = _info.find('Rating')
	if temp != None:
		info['rating'] = temp.text
	temp = _info.find(".//boxart[@side='front']")
	if temp != None:
		info['boxart'] = temp.attrib['thumb']
	
	return info

def request():
	#18266 games on TheGamesDB
	_ids = []

	_gamesList = requests.get(gamesDBWAPI+'GetPlatformGames.php?platform=1')
	_gameElements = ET.fromstring(_gamesList.text.encode('utf-8')).findall('Game')
	print "game elements: %d" % len(_gameElements)
	for _game in _gameElements:
		_ids.append( int(_game.find('id').text) )
	print "Games in list: %d" % len(_ids)

	for i in _ids:
		print "parsing game %d" % i
		#retrieve game info by ID
		_gameInfo = requests.get(gamesDBWAPI+'GetGame.php?id=%d'%i)
		_gI = ET.fromstring(_gameInfo.text.encode('utf-8')).find('Game')
		if _gI != None:
			gameInfo = extractGameInfo(_gI)
			with open("IDs.txt","a") as file:
				file.write(str(i) + ' ' + gameInfo['name'].encode('utf-8')+'\n')
			
			#create XML elements
			root = ET.Element('Data')
			_imgURL = ET.SubElement(root, 'baseImgUrl')
			_imgURL.text = gamesDBImgUrl
			game = ET.SubElement(root, 'Game')
			_id = ET.SubElement(game, "id")
			_id.text = str(i)
			_name = ET.SubElement(game, "GameTitle")
			_name.text = gameInfo['name']
			_platform = ET.SubElement(game, "Platform")
			_platform.text = gameInfo['platform']
			_release = ET.SubElement(game, "ReleaseDate")
			_release.text = gameInfo['release_date']
			_desc = ET.SubElement(game, "Overview")
			_desc.text = gameInfo['overview']
			_esrb = ET.SubElement(game, "ESRB")
			_esrb.text = gameInfo['ESRB']
			_players = ET.SubElement(game, "Players")
			_players.text = gameInfo['players']
			_coop = ET.SubElement(game, "Co-op")
			_coop.text = gameInfo['co-op']
			_publisher = ET.SubElement(game, "Publisher")
			_publisher.text = gameInfo['publisher']
			_developer = ET.SubElement(game, "Developer")
			_developer.text = gameInfo['developer']
			_genres = ET.SubElement(game, "Genres")
			for _genre in gameInfo['genres']:
				_gen = ET.SubElement(_genres, "genre")
				_gen.text = _genre
			_rating = ET.SubElement(game, "Rating")
			_rating.text = gameInfo['rating']
			_boxart = ET.SubElement(game, "Boxart")
			_boxart.text = gameInfo['boxart']
					
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
			#--------------------------------------------------------------
			tree = ET.ElementTree(root)
			f = open("games/g"+str(i)+".xml", "w")						#write to "games" folder
			tree.write(f, encoding='utf-8', xml_declaration=True)
			f.close()

def main():
	#steamTest()
	print "Pulling data..."
	request()
	print "DONE!"
	
if __name__ == "__main__":
	main()