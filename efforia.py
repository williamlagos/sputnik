#!/usr/bin/python
# -*- coding: utf-8 -*-
import optparse,os,sys
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

sys.path.append(os.path.abspath("efforia"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="port",help="Select a port to connect efforia platform")
(opt,args) = parser.parse_args()

import settings
from core.views import *
from play.views import *
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
			       (r"/events",   		  CalendarHandler),
			       (r"/people",   		  PeopleHandler),
			       (r"/content",     	  FeedHandler),
			       (r"/collection",   	  CollectionHandler),
			       (r"/expose",   		  UploadHandler),
			       (r"/favorites",		  FavoritesHandler),
			       (r"/config",		  	  ConfigHandler),
			       (r"/schedule",		  ScheduleHandler),		       
			       (r"/(.*)",			 FileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/")})]
		self.define_keys()
		self.application = tornado.web.Application(urlhandlers,autoescape=None,cookie_secret=True,
		twitter_consumer_key=self.twitter_key,twitter_consumer_secret=self.twitter_secret,
		facebook_api_key=self.facebook_key,facebook_secret=self.facebook_secret)
	def define_keys(self):
		self.facebook_key = '153246718126522'
		self.facebook_secret = '15f57d59a69b96c3d3013b4c9aa301f2'
		self.twitter_key = 'oUa8pDde2HDLnVfT8P8p4g'
		self.twitter_secret = 'viyd4XjO4tJ9RIjK97HVX4FSocYMv3mgjvEt5vBH28Y'

if __name__ == "__main__":
	try:
		efforia = Efforia()
		http_server = tornado.httpserver.HTTPServer(efforia.application)
		if opt.port: http_server.listen(int(opt.port))
		else: http_server.listen(8888)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt: pass
