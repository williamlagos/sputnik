#!/usr/bin/python
# -*- coding: utf-8 -*-
import optparse,os,sys

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
	efforia = Runtime([(r"/",Efforia),
	(r"/register",           Register),
	(r"/google",             GoogleHandler),
	(r"/twitter",            TwitterHandler),
	(r"/facebook",           FacebookHandler),
	(r"/login",              LoginHandler),
	(r"/logout",             LogoutHandler),
	(r"/delete",             DeleteHandler),
	(r"/fan",              	 FanHandler),
	(r"/known",              KnownHandler),
	(r"/spreads",            SpreadsHandler),
	(r"/spread",             SpreadHandler),
	(r"/causes",             CausesHandler),
	(r"/create",             CreateHandler),
	(r"/activity",           SearchHandler),
	(r"/content",            CollectionHandler),
	(r"/contents",           ContentHandler),
	(r"/collection",         CollectionHandler),
	(r"/play",               PlayHandler),
	(r"/expose",             UploadHandler),
	(r"/favorites",          FavoritesHandler),
	(r"/config",             ConfigHandler),
	(r"/schedule",           ScheduleHandler),
	(r"/profile",          	 ProfileHandler),
	(r"/password",           PasswordHandler),
	(r"/search",             SearchHandler),      
	(r"/movement",           MovementHandler),
	(r"/calendar",           CalendarHandler),
	(r"/payment",            PaymentHandler),
	(r"/cancel",           	 CancelHandler),
	(r"/products",           ProductsHandler),
	(r"/integrations",       IntegrationsHandler),
	(r"/delivery",           DeliveryHandler),
	(r"/correios",           CorreiosHandler),
	(r"/cart",               CartHandler),
	(r"/paypal",             PaypalIpnHandler),
	(r"/place",              PlaceHandler),
	(r"/(.*)",             	 Handler, {"path": os.path.join(os.path.dirname(__file__), "static/")})],'social.json')			
	efforia.run(opt.port)
