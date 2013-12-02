import requests
import os
import xml.etree.ElementTree as ET

steamWAPI = 'http://api.steampowered.com/'
steamKEY = 'B1B2EF4AFBA86C6A4DB4DCF4A282BBFB'
NAMES = []
IDS = []

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def getSteamGames():
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
	games1, games2 = [], []
	for game in games:
		name = game[1].text.encode('utf-8')
		playtime2weeks=''
		playtimeForever=''
		if name in NAMES:
			if (game[2].tag == 'playtime_2weeks') & (game[3].text != str(0)):
				playtime2weeks = int(game[2].text)
				playtimeForever = int(game[3].text)
				games1.append((IDS[NAMES.index(name)], name, playtime2weeks, playtimeForever))
			elif (game[2].text != str(0)):
				playtime2weeks = 0
				playtimeForever = int(game[2].text)
				games2.append((IDS[NAMES.index(name)], name, playtime2weeks, playtimeForever))
				
	games1 = sorted(games1, key=lambda x:x[2], reverse=True)
	games2 = sorted(games2, key=lambda x:x[3], reverse=True)
	return (games1 + games2)

#def getSimilarGames(id):
	#files = os.listdir("ranks/")
	#print type(id)
	#print files
	#for file in files:
		#print file.split('.txt')[0]
		#if id == file.split('.txt')[0]:
			#with open("ranks/{}".format(file),'r') as f:
				#for i in range(5):
					#print '\t{}\n'.format(f.readline())
	
	

def main():
	#	withdraw DB index
	with open("IDs.txt", 'r') as file:
		for line in file:
			data = line.split(' ', 1)
			NAMES.append(data[1].rstrip())
			IDS.append(data[0])
			
	games = getSteamGames()
	for game in games:
		print game[0], game[1], game[2], game[3]
		#getSimilarGames(game[0])

if __name__ == '__main__':
	main()