#!/usr/bin/python
# -*- coding: utf-8 -*-
import optparse,os,sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import simplejson as json

sys.path.append(os.path.abspath("efforia"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="port",help="Select a port to connect efforia platform")
(opt,args) = parser.parse_args()

import settings
from core.views import *
from core.social import *
from play.views import *
from create.views import *
from spread.views import *
from explore.views import *

class Efforia():
	def __init__(self):
		urlhandlers = [(r"/", 			  SocialHandler),
			       (r"/google",   		  GoogleHandler),
			       (r"/twitter",   		  TwitterHandler),
			       (r"/facebook", 		  FacebookHandler),
			       (r"/register", 		  RegisterHandler),
			       (r"/login",    		  LoginHandler),
			       (r"/logout",   		  LogoutHandler),
			       (r"/know/",    		  KnownHandler),
		    	   (r"/spread",   		  SpreadHandler),
		    	   (r"/causes",   		  CausesHandler),
			       (r"/spreads",  		  PostHandler),
			       (r"/activity",  		  SearchHandler),
			       (r"/content",     	  CollectionHandler),
			       (r"/contents",     	  ContentHandler),
			       (r"/collection",   	  CollectionHandler),
			       (r"/expose",   		  UploadHandler),
			       (r"/favorites",		  FavoritesHandler),
			       (r"/config",		  	  ConfigHandler),
			       (r"/schedule",		  ScheduleHandler),
			       (r"/profile",		  ProfileHandler),
			       (r"/password",		  PasswordHandler),
			       (r"/search",			  SearchHandler),      
			       (r"/movement",		  MovementHandler),
			       (r"/calendar",		  CalendarHandler),
			       (r"/(.*)",			  FileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/")})]
		apis = json.load(open('social.json','r'))
		self.application = tornado.web.Application(urlhandlers,autoescape=None,cookie_secret=True,
		twitter_consumer_key=apis['twitter']['client_key'],twitter_consumer_secret=apis['twitter']['client_secret'],
		facebook_api_key=apis['facebook']['client_key'],facebook_secret=apis['facebook']['client_secret'])

if __name__ == "__main__":
	try:
		efforia = Efforia()
		http_server = tornado.httpserver.HTTPServer(efforia.application)
		if opt.port: http_server.listen(int(opt.port))
		else: http_server.listen(8888)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt: pass
