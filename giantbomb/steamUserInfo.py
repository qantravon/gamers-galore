import requests
import urllib2
import datetime
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

steamWAPI = 'http://api.steampowered.com/'
steamKEY = 'B1B2EF4AFBA86C6A4DB4DCF4A282BBFB'

def steamTest():
	STEAM_USERNAME = 'qantravon'
	id = '76561197994932142'
	username_r = requests.get('http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(STEAM_USERNAME))
	steamid = str(parseString(username_r.text.encode('utf-8')).getElementsByTagName('steamID64')[0].firstChild.wholeText)
	print steamid
	playerStats = requests.get(steamWAPI+'IPlayerService/GetOwnedGames/v0001/?key='+steamKEY+'&steamids='+id+'&include_played_free_games=true&format=xml')
	stats = ET.fromstring(playerStats.read())
	print stats

def main():
	steamTest()

if __name__ == '__main__':
	main()