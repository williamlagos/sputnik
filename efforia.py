import django.core.handlers.wsgi
import sys,os

sys.path.append(os.path.abspath("efforia"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import settings
import stream
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

from play import video
from spread import social,auth

django_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
urlhandlers = [(r"/", social.SocialHandler),
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
	       (r"/know/",    social.KnownHandler),
	       (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/")}),
	       ('.*', tornado.web.FallbackHandler, dict(fallback=django_app))]


google_consumer_key = "efforia.herokuapp.com"
google_consumer_secret = "Cr3FMHrhTrMpZVFjHXP8IUSC"
application = tornado.web.Application(urlhandlers,autoescape=None,cookie_secret=True,
google_consumer_key=google_consumer_key,google_consumer_secret=google_consumer_secret)

if __name__ == "__main__":
	try:
		http_server = tornado.httpserver.HTTPServer(application)
		http_server.listen(int(sys.argv[1]))
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print "Exitting efforia platform"
