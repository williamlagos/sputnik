#!/usr/bin/python
# -*- coding: utf-8 -*-
from forms import CausesForm
from models import *
from coronae import append_path
from unicodedata import normalize 
append_path()

import urllib

from core.social import TwitterHandler
from play.models import Playable
from core.views import *

class CreateHandler(Efforia):
    def get(self):
        self.srender("create.html")

class CausesHandler(Efforia,TwitterHandler):
    def get(self):
        if 'view' in self.request.arguments:
            strptime,token = self.get_argument('object').split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            spreaded = globals()[rel].objects.all().filter(date=now)[0]
            feed = []; feed.append(spreaded.spreaded)
            spreads = globals()[rel].objects.all().filter(spreaded=spreaded.spreaded)
            for s in spreads: feed.append(s.spread)
            self.render_grid(feed)
        else:
            form = CausesForm()
            form.fields['title'].label = 'Título da causa'
            form.fields['content'].initial = 'Descreva o que você pretende atingir nesta causa, de uma forma bastante breve.'
            form.fields['end_time'].label = 'Prazo final'
            self.srender("causes.html",form=form)
    def post(self):
        token = '%s' % self.get_argument('token')
        name = u'%s' % self.get_argument('title')
        title = "#%s" % name.replace(" ","")
        text = u"%s " % self.get_argument("content")
        video = Playable.objects.all().filter(token=token)[0]
        end_time = datetime.strptime(self.get_argument('deadline'),'%d/%m/%Y')
        cause = Causable(name='#'+name,user=self.current_user(),play=video,content=text,end_time=end_time)
        cause.save()
        twitter = self.current_user().profile.twitter_token
        if twitter:
            token = self.format_token(twitter)
            self.twitter_request(path="/statuses/update",access_token=token,
                                 callback=self.async_callback(self.on_post),post_args={"status": text+title})
        causes = Causable.objects.all().filter(user=self.current_user())
        self.accumulate_points(1)
        return self.srender('grid.html',feed=causes)
    def on_post(self,response):
        self.finish()

class MovementHandler(Efforia):
    def get(self):
        if "action" in self.request.arguments:
            feed = []; feed.append(Action('movement'))
            causes = Causable.objects.all().filter(user=self.current_user())
            for c in causes:
                c.name = '%s#' % c.name 
                feed.append(c)
            self.render_grid(feed)
        elif 'view' in self.request.arguments:
            move = Movement.objects.all(); feed = []; count = 0
            for m in move.values('name').distinct():
                if 'grid' not in self.get_argument('view'):
                    if not count: feed.append(Action('play')) 
                    feed.append(move.filter(name=m['name'],user=self.current_user())[0].cause)
                else:
                    if not count: feed.append(Action('new##')) 
                    feed.append(move.filter(name=m['name'],user=self.current_user())[0])
                count += 1
            self.render_grid(feed)
        else: 
            move = Movement.objects.all().filter(user=self.current_user)
            message = ""
            if not len(move):
                message = "Você não possui nenhum movimento. Gostaria de criar um?"
            else:
                scheds = len(Movement.objects.filter(user=self.current_user()).values('name').distinct())
                message = '%i Movimentos em aberto' % scheds
            return self.srender('message.html',message=message,visual='crowd.png',tutor='Os movimentos são uma forma fácil de acompanhar todas as causas do Efforia em que você apoia. Para utilizar, basta selecioná-las e agrupá-las num movimento.')
    def post(self):
        causables = []
        objects = self.get_argument('objects')
        title = self.get_argument('title')
        objs = urllib.unquote_plus(objects).split(',')
        for o in objs: 
            strptime,token = o.split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            causables.append(globals()[obj].objects.all().filter(date=now)[0])
        for c in causables: 
            move = Movement(user=self.current_user(),cause=c,name='##'+title)
            move.save()
        self.accumulate_points(1)
        moves = len(Movement.objects.all().filter(user=self.current_user()).values('name').distinct())
        return self.srender('message.html',message='%i Movimentos em aberto' % moves,visual='crowd.png',tutor='Os movimentos são uma forma fácil de acompanhar todas as causas do Efforia em que você apoia. Para utilizar, basta selecioná-las e agrupá-las num movimento.')
