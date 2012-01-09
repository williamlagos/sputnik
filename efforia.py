from django.conf import settings
settings.configure(DATABASE_ENGINE='sqlite3', DATABASE_NAME='dev.db',
                   INSTALLED_APPS=('django.contrib.contenttypes',
                                   'django.contrib.auth',
                                   'django.contrib.sessions'))

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web

from play import video
from spread import social,register

app = tornado.web.Application([
    (r"/", social.ProfileHandler),
    (r"/register/", register.RegisterHandler),
    (r"/login/",    social.GoogleHandler),
    (r"/logout/",   social.ProfileHandler),
    (r"/spread/",   social.SpreadHandler),
    (r"/spreads/",  social.SpreadHandler),
    (r"/search/",   social.SearchHandler),
    (r"/people/",   social.ProfileHandler),
    (r"/know/",     social.KnownHandler),
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static/")}),
    (r"/play/",     video.PlayerHandler),],
    autoescape=None)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
