#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os,optparse
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
from play import video
from spread import social,auth

class Efforia():
	def __init__(self):
		self.django_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
		urlhandlers = [(r"/", social.SocialHandler),
				   (r"/oauth2",   auth.GoogleOAuth2Handler),
				   (r"/oauth2callback",   auth.OAuth2Handler),
			       (r"/google",   auth.GoogleHandler),
			       (r"/facebook", auth.FacebookHandler),
			       (r"/register", auth.RegisterHandler),
			       (r"/login",    auth.LoginHandler),
			       (r"/logout",   auth.LogoutHandler),
		    	   (r"/spread",   social.SpreadHandler),
			       (r"/spreads",  social.PostHandler),
			       (r"/search",   social.SearchHandler),
			       (r"/people",   social.PeopleHandler),
			       (r"/play",     video.PlayerHandler),
			       (r"/expose",   video.UploadHandler),
			       (r"/know/",    social.KnownHandler),
			       (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/")}),
			       ('.*', tornado.web.FallbackHandler, dict(fallback=self.django_app))]
		self.application = tornado.web.Application(urlhandlers,autoescape=None,cookie_secret=True)

if __name__ == "__main__":
	try:
		efforia = Efforia()
		http_server = tornado.httpserver.HTTPServer(efforia.application)
		if opt.port: http_server.listen(int(opt.port))
		else: http_server.listen(8888)
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt: pass