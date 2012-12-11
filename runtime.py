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
	(r"/spreads",            SpreadsHandler),
	(r"/create",             CreateHandler),
	(r"/play",               PlayHandler),
	(r"/explore",             SearchHandler),      
	(r"/register",           Register),
	(r"/google",             GoogleHandler),
	(r"/twitter",            TwitterHandler),
	(r"/facebook",           FacebookHandler),
	(r"/login",              LoginHandler),
	(r"/logout",             LogoutHandler),
	(r"/delete",             DeleteHandler),
	(r"/fan",              	 FanHandler),
	(r"/known",              KnownHandler),
	(r"/activity",           SearchHandler),
	(r"/content",            CollectionHandler),
	(r"/collection",         CollectionHandler),
	(r"/collect",         	 CollectHandler),
	(r"/expose",             UploadHandler),
	(r"/favorites",          FavoritesHandler),
	(r"/config",             ConfigHandler),
	(r"/schedule",           ScheduleHandler),
	(r"/profile",          	 ProfileHandler),
	(r"/password",           PasswordHandler),
	(r"/payment",            PaymentHandler),
	(r"/cancel",           	 CancelHandler),
	(r"/integrations",       IntegrationsHandler),
	(r"/delivery",           DeliveryHandler),
	(r"/correios",           CorreiosHandler),
	(r"/cart",               CartHandler),
	(r"/paypal",             PaypalIpnHandler),
	(r"/place",              PlaceHandler),
	(r"/userid",             IdHandler),
        ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app))])
	efforia.run(opt.port)
