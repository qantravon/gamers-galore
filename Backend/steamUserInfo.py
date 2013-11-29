import requests
import urllib2
import datetime
import xml.etree.ElementTree as ET

steamWAPI = 'http://api.steampowered.com/'
NAMES = []
IDS = []

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def steamTest():
	STEAM_USERNAME = raw_input('Input numeric SteamID, or your Steam Community name ---> ')

	#id = '76561197979836184'
	steamid=''
	if is_number(STEAM_USERNAME) == False:
		username_r = requests.get('http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(STEAM_USERNAME))
		steamid = (ET.fromstring(username_r.text.encode('utf-8'))).find('steamID64').text
	else:
		steamid = STEAM_USERNAME

	req = steamWAPI+'IPlayerService/GetOwnedGames/v0001/?key='+steamKEY+'&steamid='+steamid+'&include_appinfo=1&include_played_free_games=1&format=xml'

	playerGames = requests.get(req)
	games = ET.fromstring(playerGames.text.encode('utf-8')).find('games')
	print 'ID, Name, 2weeks playtime, forever playtime'
	for game in games:
		id = game[0].text
		name = game[1].text.encode('utf-8')
		playtime2weeks=''
		playtimeForever=''
		if name in NAMES:
			if game[2].tag == 'playtime_2weeks':
				playtime2weeks = game[2].text
				playtimeForever = game[3].text
			else:
				playtime2weeks = 0
				playtimeForever = game[2].text

			if (playtimeForever != str(0)) & (id != None):
				print id, name, playtime2weeks, playtimeForever

	print '\n\n'

			

def main():
	#	withdraw DB index
	with open("IDs.txt", 'r') as file:
		for line in file:
			data = line.split(' ', 1)
			NAMES.append(data[1].rstrip())
			IDS.append(data[0])
			
	steamTest()

if __name__ == '__main__':
	main()