import django.core.handlers.wsgi
from django.conf import settings
settings.configure(DATABASE_ENGINE='django.db.backends.postgresql_psycopg2', DATABASE_NAME='dev.db',
                   INSTALLED_APPS=('play','spread',
                                   'django.contrib.contenttypes',
                                   'django.contrib.auth',
                                   'django.contrib.sessions'),
		   ROOT_URLCONF = 'urls')

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

from play import video
from spread import social,auth

django_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
application = tornado.web.Application([
    (r"/", social.ProfileHandler),
    (r"/register", auth.RegisterHandler),
    (r"/login",    auth.LoginHandler),
    (r"/logout",   auth.LogoutHandler),
    (r"/spread",   social.SpreadHandler),
    (r"/spreads",  social.SpreadHandler),
    (r"/search",   social.SearchHandler),
    (r"/people",   social.PeopleHandler),
    (r"/know",     social.KnownHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/")}),
    (r"/play",     video.PlayerHandler),
    ('.*', tornado.web.FallbackHandler, dict(fallback=django_app)),],
    autoescape=None,cookie_secret=True)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
