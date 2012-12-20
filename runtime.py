#!/usr/bin/python
# -*- coding: utf-8 -*-
import optparse,os,sys
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import simplejson as json
sys.path.append(os.path.abspath("static"))
sys.path.append(os.path.abspath("efforia"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
parser = optparse.OptionParser()
parser.add_option("-p", "--port", dest="port",help="Select a port to connect efforia platform")
(opt,args) = parser.parse_args()

import settings
from coronae import Runtime
from core.views import *
from core.social import *
from play.views import *
from create.views import *
from spread.views import *
from explore.views import *
from store.views import *

if __name__ == "__main__":
	wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
	efforia = Runtime([
	(r"/google",             GoogleHandler),
	(r"/twitter",            TwitterHandler),
	(r"/facebook",           FacebookHandler),
	(r"/twitter_post",		 TwitterPosts),
	(r"/facebook_post",		 FacebookPosts),
	(r"/facebook_event",	 FacebookEvents),      
	(r"/register",           Register),
    ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app))],'social.json')
	efforia.run(opt.port)
