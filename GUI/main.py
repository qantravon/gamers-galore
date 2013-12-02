#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import json
import os
import urllib3
import logging
import xml.etree.ElementTree as ET
from google.appengine.ext.webapp import template
from google.appengine.api import images


#----------------------------GLOBAL VARS------------------------------------------------------
steamWAPI = 'http://api.steampowered.com/'
steamKEY = 'B1B2EF4AFBA86C6A4DB4DCF4A282BBFB'
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
IDS = []
NAMES = []
#---------------------------END GLOBAL VARS--------------------------------------------------------


#---------------------------GLOBAL FUNCTIONS---------------------------------------------------	
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def indexDB():
	with open("IDs.txt", 'r') as file:
		for line in file:
			data = line.split(' ', 1)
			NAMES.append(data[1].rstrip())
			IDS.append(data[0])
		
def getSteamGames(steamid):
	#id = '76561197979836184' testing for shane's account
	indexDB()
	req = steamWAPI+'IPlayerService/GetOwnedGames/v0001/?key='+steamKEY+'&steamid='+steamid+'&include_appinfo=1&include_played_free_games=1&format=xml'
	http = urllib3.PoolManager()
	playerGames = http.request('get', req)
	games = ET.fromstring(playerGames.data).find('games')
	games1, games2 = [], []
	
	for game in games:
		name = game[1].text.encode('utf-8')
		if name in NAMES:
			playtime2weeks=''
			playtimeForever=''
			image = ''
			gameIndex = NAMES.index(name)
			root = ET.parse('games/'+IDS[gameIndex]+'.xml').getroot()
			logging.info(name + " id: %d" % gameIndex)
			_image = root.find('image')
			image = ""
			if _image != None:
				image = _image.text
			if image == "":
				image = "image location not found"
			logging.debug(image)
			#images work for a few games, but most are not parsing correctly
			if (game[2].tag == 'playtime_2weeks') & (game[3].text != str(0)):
				playtime2weeks = int(game[2].text)
				playtimeForever = int(game[3].text)
				games1.append((IDS[gameIndex], name, playtime2weeks, playtimeForever, image))
			elif (game[2].text != str(0)):
				playtime2weeks = 0
				playtimeForever = int(game[2].text)
				games2.append((IDS[gameIndex], name, playtime2weeks, playtimeForever, image))
				
	games1 = sorted(games1, key=lambda x:x[2], reverse=True)
	games2 = sorted(games2, key=lambda x:x[3], reverse=True)
	return (games1 + games2)
#----------------------------END GLOBAL FUNCTIONS--------------------------------------------------------
	

#--------------------------------------------------------------------------------------------------------
#----------------------------MAIN HANDLER----------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------	
class MainHandler(webapp2.RequestHandler):
    

    def get(self):

        self.response.write(template.render('main.html', {}))
        
    def post(self):
		STEAM_USERNAME = self.request.get('user_name')
		steamid=''
		if is_number(STEAM_USERNAME) == False:
			http = urllib3.PoolManager()
			username_r = http.request('get', 'http://steamcommunity.com/id/{0}/games?tab=all&xml=1'.format(STEAM_USERNAME))
			steamid = ((ET.fromstring(username_r.data)).find('steamID64')).text
		else:
			steamid = STEAM_USERNAME
			
		games = getSteamGames(steamid)
		
		results = {
			'simgames':["e","f","g","h"],
			'username': STEAM_USERNAME,
			'steam_id': steamid,
			'gamezz': games,
			'games':[("1",33,"http://static.giantbomb.com/uploads/scale_avatar/9/93770/2370498-genesis_desertstrike_2__1_.jpg"),
					("2",34,"http://static.giantbomb.com/uploads/scale_avatar/0/238/707495-the_real_deal_2.jpg"),
					("3",44,"http://static.giantbomb.com/uploads/scale_avatar/0/1614/969857-metal_slug_x_ng_us.jpg"),
					("4",555,"http://static.giantbomb.com/uploads/scale_avatar/10/103881/1803050-ar.jpg")],
			'simimages':["11","12","22","333"]}
			
		template = JINJA_ENVIRONMENT.get_template('results.html')
		self.response.write(template.render(results))
#------------------------------------------------------------------------------------------------------------
#-------------------------END MAIN HANDLER-------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
