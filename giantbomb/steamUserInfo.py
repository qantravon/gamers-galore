import requests
import urllib2
import datetime
import xml.etree.ElementTree as ET

steamWAPI = 'http://api.steampowered.com/'
names = []
ids = []

def steamTest():
	STEAM_USERNAME = 'qantravon'
	#id = '76561197994932142'
	username_r = requests.get('http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(STEAM_USERNAME))
	steamid = (ET.fromstring(username_r.text.encode('utf-8'))).find('steamID64').text
	
	#shaneID = '76561197979836184'
	req = steamWAPI+'IPlayerService/GetOwnedGames/v0001/?key='+steamKEY+'&steamid='+steamid+'&include_appinfo=1&include_played_free_games=1&format=xml'

	playerGames = requests.get(req)
	games = ET.fromstring(playerGames.text.encode('utf-8')).find('games')
	for game in games:
		id = game[0].text
		name = game[1].text.encode('utf-8')
		if game[2].tag == 'playtime_2weeks':
			playtime2weeks = game[2].text
			playtimeForever = game[3].text
		else:
			playtime2weeks = 0
			playtimeForever = game[2].text
		print id, name, playtime2weeks, playtimeForever
		if name in names:
			print 'SUCCESS!'
		else:
			print 'FAILURE!'
			
	#games = (ET.fromstring(stats.text.encode('utf-8'))).find('games')
	#for game in games:
		#print game.find('name').text

	
	#stats = ET.fromstring(playerStats.text.encode('utf-8')).find('games')
	#for game in stats:
		#print game[1].text

def main():
	with open("IDs.txt", 'r') as file:
		for line in file:
			data = line.split()
			names.append(data[1])
			ids.append(data[0])
			
	steamTest()

if __name__ == '__main__':
	main()