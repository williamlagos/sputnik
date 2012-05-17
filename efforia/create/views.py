#!/usr/bin/python
# -*- coding: utf-8 -*-
from tornado.auth import TwitterMixin
from forms import CausesForm
from stream import StreamService
from handlers import append_path
from unicodedata import normalize 
append_path()

from play.models import Playable
from spread.views import SocialHandler

class CausesHandler(SocialHandler,TwitterMixin):
    def get(self):
        form = CausesForm()
        self.srender("create.html",form=form)
    def post(self):
        token = '%s' % self.get_cookie('token')
        name = u'%s' % self.get_argument('title')
        title = "#%s" % name.replace(" ","")
        text = u"%s " % self.get_argument("content")
        keys = ','
        keywords = self.get_argument('keywords').split(' ')
        for k in keywords: k = normalize('NFKD',k.decode('utf-8')).encode('ASCII','ignore')
        keys = keys.join(keywords)
        video = Playable.objects.all().filter(token=token)
        return
        cred = self.twitter_credentials()
        self.twitter_request(path="/statuses/update",access_token=cred,
                             callback=self.async_callback(self.on_post),post_args={"status": text+title})
    def on_post(self,response):
        self.finish()