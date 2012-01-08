from django.conf import settings
settings.configure(DATABASE_ENGINE='sqlite3', DATABASE_NAME='dev.db')
import django.contrib.auth.views
import tornado.httpserver
import tornado.ioloop
import tornado.web

from play import *
from spread import social

app = tornado.web.Application([
    (r"/", social.ProfileHandler),
    #('^register/$', 'spread.register.newuser'),
    (r"/login/",    social.ProfileHandler),
    (r"/logout/",   django.contrib.auth.views.logout),
    (r"/spread/",   social.SpreadHandler),
    (r"/spreads/",  social.SpreadHandler),
    (r"/search/",   social.SearchHandler),
    (r"/people/",   social.ProfileHandler),
    (r"/know/",     social.KnownHandler),
    #('^play/$',     'play.video.playvideo'),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
