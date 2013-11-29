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
from google.appengine.ext.webapp import template
from google.appengine.api import images


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    

    def get(self):

        self.response.write(template.render('main.html', {}))
        
    def post(self):
        username = self.request.get('user_name')
    	results = {
            'simgames':["e","f","g","h"],
            'username': username,
            'games':[("1",33,"http://static.giantbomb.com/uploads/scale_avatar/9/93770/2370498-genesis_desertstrike_2__1_.jpg"),
                     ("2",34,"http://static.giantbomb.com/uploads/scale_avatar/0/238/707495-the_real_deal_2.jpg"),
                     ("3",44,"http://static.giantbomb.com/uploads/scale_avatar/0/238/707495-the_real_deal_2.jpg"),
                     ("4",555,"http://static.giantbomb.com/uploads/scale_avatar/0/238/707495-the_real_deal_2.jpg")
                    ],
            #'games': [33,34,44,555],
            #'images': ["http://static.giantbomb.com/uploads/scale_avatar/9/93770/2370498-genesis_desertstrike_2__1_.jpg",
            #           "https://scontent-b-dfw.xx.fbcdn.net/hphotos-ash3/643899_10151224644799740_33181706_n.jpg",
            #           "https://scontent-b-dfw.xx.fbcdn.net/hphotos-ash3/643899_10151224644799740_33181706_n.jpg",
            #           "https://scontent-b-dfw.xx.fbcdn.net/hphotos-ash3/643899_10151224644799740_33181706_n.jpg"],
            
            'simimages':["11","12","22","333"]
            #'gamesid':["1","2","3","4","5"]
            #'times':[]
            }
        template = JINJA_ENVIRONMENT.get_template('results.html')
        self.response.write(template.render(results))
    	#self.response.out.write(template.render('results.html',{}))
    	#self.response.out.write(template.render('results.html',{'Test.xml'}))

    



      		



app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
