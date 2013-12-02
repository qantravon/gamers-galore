#merging gamesDB with giantbombDB

import xml.etree.ElementTree as ET
import os


IDindex = 41804


def extractGameNames(_folder):
	names=[]
	ids=[]
	with open(_folder, 'r') as file:
		for line in file:
			data = line.split(' ',1)
			#print data[0]
			names.append(data[1].rstrip())
			ids.append(data[0])
	return names, ids

#def compareGameInfo(id, _id):
	#root1 = ET.parse("Backend/games/"+id+".xml").getroot()
	#root2 = (ET.parse("TheGamesDB/games/g"+_id+".xml").getroot()).find('Game')
	#if root1[2].text == None:
		#if root2[4].text != None:
			#root1[2].text = root2[1].text
	#for genre in root2[2]:
		#if genre.text in root1[3]

def addGame(id):
	global IDindex
	game = (ET.parse("TheGamesDB/games/g"+id+".xml").getroot()).find('Game')
	if game[4].text != None:
		root = ET.Element("root")
		_id = ET.SubElement(root, "id")
		_id.text = str(IDindex)
		IDindex+=1
		_name = ET.SubElement(root, "name")
		_name.text = game[1].text
		_desc = ET.SubElement(root, "description")
		_desc.text = game[4].text
		_genres = ET.SubElement(root, "genres")
		for _genre in game[10]:
			_gen = ET.SubElement(_genres, "genre")
			_gen.text = _genre.text
		_image = ET.SubElement(root, "image")
		if game[12].text != None:
			_image.text = "http://thegamesdb.net/banners/"+game[12].text
		tree = ET.ElementTree(root)
		#print tree
		with open("Backend/IDs.txt", 'a') as file:
			file.write(_id.text+' '+_name.text.encode('utf-8')+'\n')
		with open("Backend/games/"+_id.text+".xml", 'w') as file:
			tree.write(file, encoding='utf-8', xml_declaration=True)


def main():
	currentGameNames, currentGameIDs = extractGameNames("Backend/IDs.txt")
	newGameNames, newGameIDs = extractGameNames("TheGamesDB/IDs.txt")

	for _newName in newGameNames:
		if _newName not in currentGameNames:		#add game to back of database
			addGame(newGameIDs[newGameNames.index(_newName)])



if __name__ == '__main__':
	main()