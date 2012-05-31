#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from handlers import append_path
from stream import StreamService
append_path()

import tornado.web,re
import simplejson as json
from tornado import httpclient
from models import *
from unicodedata import normalize
from create.models import Causable
from core.models import Profile
from spread.views import SocialHandler
from StringIO import StringIO

objs = json.load(open('objects.json','r'))

class CollectionHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        count = len(Playable.objects.all().filter(user=self.current_user()))
        message = '%i Vídeos disponíveis em sua coleção para tocar.' % count
        self.render(self.templates()+'collection.html',message=message)
    def post(self):
        if not self.authenticated(): return
        videos = Playable.objects.all().filter(user=self.current_user())
        self.srender('grid.html',feed=videos)

class UploadHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        description = ''; token = '!!'
        for k in self.request.arguments.keys(): description += '%s;;' % self.request.arguments[k][0]
        t = token.join(description[:-2].split())
        self.clear_cookie('description')
        self.set_cookie('description',t)
    def post(self):
        content = re.split(';;',self.get_cookie('description').replace('!!',' ').replace('"',''))
        text,keywords,category,title = content
        category = int(category); keys = ','
        keywords = keywords.split(' ')
        for k in keywords: k = normalize('NFKD',k.decode('utf-8')).encode('ASCII','ignore')
        keys = keys.join(keywords)
        service = StreamService()
        response = service.video_entry(title,text,keys)
        video_io = StringIO()
        video = self.request.files['Filedata'][0]
        video_io.write(video['body'])
        resp = service.insert_video(response,video_io,video["content_type"])
        token = resp.GetSwfUrl().split('/')[-1:][0].split('?')[0]
        playable = Playable(user=self.current_user(),name='>'+title+';'+keys,description=text,token=token,category=category)
        playable.save()
        self.accumulate_points(1)
        self.set_cookie('token',token)
        self.write(token)

class ScheduleHandler(SocialHandler):
    def get(self):
        if 'action' in self.request.arguments:
            sched = Schedule.objects.all(); feed = []
	    for s in sched.values('name').distinct(): feed.append(sched.filter(name=s['name'],user=self.current_user())[0])
            return self.srender('grid.html',feed=feed)
        elif 'view' in self.request.arguments:
            name = self.request.arguments['title'][0]; play = []
            sched = Schedule.objects.all().filter(user=self.current_user,name='>>'+name) 
            for s in sched: play.append(s.play)
            self.srender('grid.html',feed=play,number=len(play))
        else: 
            play = Schedule.objects.all().filter(user=self.current_user)
            message = ""
            if not len(play):
                message = "Você não possui nenhuma programação no momento. Gostaria de criar uma?"
            else:
                scheds = len(Schedule.objects.filter(user=self.current_user()).values('name').distinct())
                message = '%i Programações de vídeos disponíveis' % scheds
            return self.srender('message.html',message=message)
    def post(self):
        playables = []
        objects = self.get_argument('objects')
        title = self.get_argument('title')
        objs = urllib.unquote_plus(str(objects)).split(',')
        for o in objs: playables.append(Playable.objects.all().filter(token=o)[0])
        for p in playables: 
            playsched = Schedule(user=self.current_user(),play=p,name='>>'+title)
            playsched.save()
	self.accumulate_points(1)
        scheds = len(Schedule.objects.all().filter(user=self.current_user(),name=title))
        return self.srender('message.html',message='%i Programações de vídeos disponíveis' % scheds)
