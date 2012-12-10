#!/usr/bin/python
# -*- coding: utf-8 -*-
from forms import CausesForm
from models import *
from coronae import append_path
from unicodedata import normalize 
append_path()

import urllib

from core.social import *
from play.models import Playable
from core.views import *

class CreateHandler(Efforia):
    def get(self):
        if 'object' in self.request.arguments:
            o,t = self.request.arguments['object'][0].split(';')
            now,objs,rel = self.get_object_bydate(o,t)
            obj = globals()[objs].objects.all().filter(date=now)
            self.get_donations(obj)
        else: self.srender("create.html")
    def post(self):
        value = int(self.request.arguments['credits'][0])
        o,t = self.request.arguments['object'][0].split(';')
        now,objs,rel = self.get_object_bydate(o,t)
        obj = globals()[objs].objects.all().filter(date=now)[0]
        don = CausableDonated(value=value,donator=self.current_user(),cause=obj)
        don.save()
        self.get_donations(obj)
    def get_donations(self,cause):
        donations = list(CausableDonated.objects.all().filter(cause=cause))
        self.render_grid(donations)
        

class CausesHandler(Efforia,TwitterHandler):
    # TODO: Fazer ponte entre request handlers do Tornado e Django
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
        credit = int(self.request.arguments['credit'][0])
        token = '%s' % self.get_argument('token')
        name = u'%s' % self.get_argument('title')
        title = "#%s" % name.replace(" ","")
        text = u"%s " % self.get_argument("content")
        video = Playable.objects.all().filter(token=token)[0]
        end_time = datetime.strptime(self.get_argument('deadline'),'%d/%m/%Y')
        cause = Causable(name='#'+name,user=self.current_user(),play=video,content=text,end_time=end_time,credit=credit)
        cause.save()
        twitter = self.current_user().profile.twitter_token
        if not twitter: twitter = get_offline_access()['twitter_token']
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
            if 'grid' in self.get_argument('view'):
                for m in move.values('name').distinct():
                    if not count: feed.append(Action('new##'))
                    feed.append(move.filter(name=m['name'],user=self.current_user())[0])
                    count += 1
            else:
                name = '##%s' % self.request.arguments['title'][0]
                feed.append(Action('play'))
                for m in move.filter(name=name,user=self.current_user()): feed.append(m.cause)
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
