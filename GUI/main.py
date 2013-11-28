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


#class MainHandler(webapp2.RequestHandler):
    #def get(self):
        #self.response.write(template.render('main.html', {}))
class MainPage(webapp2.RequestHandler):
    #def get(self):
        #guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)
        #greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        #greetings = greetings_query.fetch(10)

        #if users.get_current_user():
            #url = users.create_logout_url(self.request.uri)
            #url_linktext = 'Logout'
        #else:
            #url = users.create_login_url(self.request.uri)
            #url_linktext = 'Login'

        #template_values = {
            #'greetings': greetings,
            #'guestbook_name': urllib.quote_plus(guestbook_name),
            #'url': url,
            #'url_linktext': url_linktext,
        #}

        #template = JINJA_ENVIRONMENT.get_template('results.html')
        #self.response.write(template.render(template_values))		
	def get(self):
		self.response.write(template.render('main.html',{}))
	
	def post(self):
		username = self.request.get('user_name')
    	#self.response.out.write('Hollow ' + username)
		results = {
			'username': username,
			'id': 333444555,
			'desc': 'hello there my name is shane'
			}
		
		
		
		template = JINJA_ENVIRONMENT.get_template('results.html')
		self.response.write(template.render(results))
		#self.response.write(json.dumps(results))
    	#self.response.out.write(template.render('Test.xml',{}))
    	#self.response.out.write(template.render('results.html','Test.xml'))



      		



app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
