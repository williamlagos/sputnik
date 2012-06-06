#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from handlers import append_path
append_path()

import tornado.web,re
import simplejson as json
from tornado import httpclient
from models import *
from datetime import datetime
from unicodedata import normalize
from core.stream import StreamService
from create.models import Causable
from core.models import Profile
from spread.views import SocialHandler,Action
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
        self.title = self.keys = self.text = ''
        self.category = 0
        if 'status' in self.request.arguments:
            status = self.request.arguments['status']
            token = self.request.arguments['id']
            date = self.get_cookie('video_date')
            last = datetime.strptime(date,'%Y%m%d%H%M%S%f')
            play = Playable.objects.all().filter(user=self.current_user(),date=last)[0]
            play.token = token
            play.save()
            self.accumulate_points(1)
            self.set_cookie('token',token)
            self.redirect('/')
        else:
            description = ''; token = '!!'
            for k in self.request.arguments.keys(): description += '%s;;' % self.request.arguments[k][0]
            t = token.join(description[:-2].split())
            self.clear_cookie('description')
            self.set_cookie('description',t)
            url,token = self.parse_upload()
            self.srender('content.html',url=url,token=token)
    def post(self):
        video_io = StringIO()
        video = self.request.files['Filedata'][0]
        video_io.write(file['body'])
        boundary = self.request.headers['Content-Type'].split(';')[1][10:]
        #service.insert_video(response,video,video["content_type"],boundary)
        return
    def parse_upload(self):
        if self.get_cookie('description'): content = re.split(';;',self.get_cookie('description').replace('!!',' ').replace('"',''))
        else: return self.write('Informação não retornada.')
        text,keywords,category,title = content
        category = int(category); keys = ','
        keywords = keywords.split(' ')
        for k in keywords: k = normalize('NFKD',k.decode('utf-8')).encode('ASCII','ignore')
        keys = keys.join(keywords)
        service = StreamService()
        access_token = self.current_user().profile.google_token
        playable = Playable(user=self.current_user(),name='>'+title+';'+keys,description=text,token='',category=category)
        playable.save()
        now = playable.date.strftime('%Y%m%d%H%M%S%f')
        self.set_cookie('video_date',value=now)
        return service.video_entry(title,text,keys,access_token)

class ScheduleHandler(SocialHandler):
    def get(self):
        if 'action' in self.request.arguments:
            #sched = Schedule.objects.all(); feed = []
            #for s in sched.values('name').distinct(): feed.append(sched.filter(name=s['name'],user=self.current_user())[0])
            feed = []; feed.append(Action('abc'))
            play = Playable.objects.all().filter(user=self.current_user())
            for p in play: feed.append(p)
            self.render_grid(feed)
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
