#!/usr/bin/python
# -*- coding: utf-8 -*-
from tornado.auth import TwitterMixin
from forms import CausesForm
from models import Causable,Movement,MovementBinding
from handlers import append_path
from unicodedata import normalize 
append_path()

import urllib

from play.models import Playable
from spread.views import SocialHandler

class CausesHandler(SocialHandler,TwitterMixin):
    def get(self):
        form = CausesForm()
        self.srender("create.html",form=form)
    def post(self):
        token = '%s' % self.get_argument('token')
        name = u'%s' % self.get_argument('title')
        title = "#%s" % name.replace(" ","")
        text = u"%s " % self.get_argument("content")
        keys = ','
        keywords = self.get_argument('keywords').split(' ')
        for k in keywords: k = normalize('NFKD',k.decode('utf-8')).encode('ASCII','ignore')
        keys = keys.join(keywords)
        video = Playable.objects.all().filter(token=token)[0]
        cause = Causable(name='#'+name,user=self.current_user(),play=video,content=text)
        cause.save()
        cred = self.twitter_credentials()
        self.twitter_request(path="/statuses/update",access_token=cred,
                             callback=self.async_callback(self.on_post),post_args={"status": text+title})
    def on_post(self,response):
        self.finish()

class MovementHandler(SocialHandler):
    def get(self):
        if "action" in self.request.arguments:
            cause = Causable.objects.all().filter(user=self.current_user)
            self.srender('movements.html',cause=cause)
        else: 
            move = Movement.objects.all().filter(user=self.current_user)
            message = ""
            if not len(move):
                message = "Você não possui nenhum movimento. Gostaria de criar um?"
            else:
                scheds = len(Movement.objects.filter(user=self.current_user()).values('name').distinct())
                message = '%i Movimentos em aberto' % scheds
            self.srender('message.html',message=message)
    def post(self):
        causables = []
        objects = self.get_argument('objects')
        title = self.get_argument('title')
        objs = urllib.unquote_plus(str(objects)).split(',')
        for o in objs: causables.append(Causable.objects.all().filter(name=o)[0])
        for c in causables: 
            move = Movement(user=self.current_user(),cause=c,name='##'+title)
            move.save()
        moves = len(Movement.objects.all().filter(user=self.current_user(),name=title))
        self.srender('message.html',message='%i Movimentos em aberto' % moves)