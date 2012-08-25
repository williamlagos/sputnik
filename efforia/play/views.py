#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from coronae import append_path
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
from core.files import Dropbox
from core.views import *
from StringIO import StringIO

objs = json.load(open('objects.json','r'))

class PlayHandler(Efforia):
    def get(self):
        self.srender('play.html')

class CollectionHandler(Efforia):
    def get(self):
        if not self.authenticated(): return
        count = len(Playable.objects.all().filter(user=self.current_user()))+len(PlayablePurchased.objects.all().filter(owner=self.current_user()))
        message = '%i Vídeos disponíveis em sua coleção para tocar.' % count
        self.render(self.templates()+'message.html',message=message,visual='collection.png',tutor='A coleção contempla todos os seus itens que você comprou ou assistiu, reunindo todos de uma forma prática e bem disposta.')
    def post(self):
        if not self.authenticated(): return
        videos = list(Playable.objects.all().filter(user=self.current_user()))
        videos.extend(list(PlayablePurchased.objects.all().filter(owner=self.current_user())))
        self.srender('grid.html',feed=videos)

class UploadHandler(Efforia):
    def get(self):
        if not self.authenticated(): return
        self.title = self.keys = self.text = ''
        self.category = 0
        if 'status' in self.request.arguments:
            service = StreamService()
            status = self.request.arguments['status']
            token = self.request.arguments['id'][0]
            access_token = self.current_user().profile.google_token
            thumbnail = service.video_thumbnail(token,access_token)
            play = Playable.objects.filter(user=self.current_user()).latest('date')
            play.visual = thumbnail
            play.token = token
            play.save()
            self.accumulate_points(1)
            self.set_cookie('token',token)
            self.redirect('/')
        else:
            description = ''; token = '!!'
            for k in self.request.arguments.keys(): description += '%s;;' % self.request.arguments[k][0]
            t = token.join(description[:-2].split())
            url,token = self.parse_upload(t)
            self.srender('content.html',url=url,token=token)
    def post(self):
        photo = self.request.files['Filedata'][0]['body']
        dropbox = Dropbox()
        link = dropbox.upload_and_share(photo)
        if 'cause' not in self.request.arguments:
            p = Profile.objects.all().filter(user=self.current_user())[0]
            p.visual = link
            p.save()
        else:
            pass
        self.write(link)
    def parse_upload(self,token):
        if token: content = re.split(';;',token.replace('!!',' ').replace('"',''))
        else: return self.write('Informação não retornada.')
        credit = 0
        if len(content) is 6: category,title,credit,text,keywords,code = content
        else:
            print content 
            category,title,text,keywords,code = content
        category = int(category); keys = ','
        keywords = keywords.split(' ')
        for k in keywords: k = normalize('NFKD',k.decode('utf-8')).encode('ASCII','ignore')
        keys = keys.join(keywords)
        playable = Playable(user=self.current_user(),name='>'+title+';'+keys,description=text,token='',category=category,credit=credit)
        playable.save()
        service = StreamService()
        access_token = self.current_user().profile.google_token
        return service.video_entry(title,text,keys,access_token)

class ScheduleHandler(Efforia):
    def get(self):
        if 'action' in self.request.arguments:
            feed = []; feed.append(Action('schedule'))
            play = Playable.objects.all().filter(user=self.current_user())
            for p in play: feed.append(p)
            self.render_grid(feed)
        elif 'view' in self.request.arguments:
            sched = Schedule.objects.all(); feed = []; count = 0
            if 'grid' in self.get_argument('view'):
                for m in sched.values('name').distinct():
                    if not count: feed.append(Action('new>>')) 
                    feed.append(sched.filter(name=m['name'],user=self.current_user())[0])
                    count += 1
            else:
                name = '>>%s' % self.request.arguments['title'][0]
                feed.append(Action('playlist'))
                for s in sched.filter(name=name,user=self.current_user()): feed.append(s.play)
            self.render_grid(feed)
        else: 
            play = Schedule.objects.all().filter(user=self.current_user)
            message = ""
            if not len(play):
                message = "Você não possui nenhuma programação no momento. Gostaria de criar uma?"
            else:
                scheds = len(Schedule.objects.filter(user=self.current_user()).values('name').distinct())
                message = '%i Programações de vídeos disponíveis' % scheds
            return self.srender('message.html',message=message,visual='schedule.png',tutor='As programações são uma forma fácil de acompanhar todos os vídeos do Efforia em que você assiste. Para utilizar, basta selecioná-los e agrupá-los numa programação.')
    def post(self):
        playables = []
        objects = self.get_argument('objects')
        title = self.get_argument('title')
        objs = urllib.unquote_plus(str(objects)).split(',')
        for o in objs: 
            strptime,token = o.split(';')
            now,obj,rel = self.get_object_bydate(strptime,token,miliseconds=True)
            playables.append(globals()[obj].objects.all().filter(date=now)[0])
        for p in playables:
            playsched = Schedule(user=self.current_user(),play=p,name='>>'+title)
            playsched.save()
        self.accumulate_points(1)
        scheds = len(Schedule.objects.all().filter(user=self.current_user()).values('name').distinct())
        return self.srender('message.html',message='%i Programações de vídeos disponíveis' % scheds,visual='schedule.png',tutor='As programações são uma forma fácil de acompanhar todos os vídeos do Efforia em que você assiste. Para utilizar, basta selecioná-los e agrupá-los numa programação.')
    
class CollectHandler(Efforia):
    def get(self):
        o,t = self.request.arguments['object'][0].split(';')
        now,objs,rel = self.get_object_bydate(o,t)
        obj = globals()[objs].objects.all().filter(date=now)[0]
        purchased = len(PlayablePurchased.objects.all().filter(owner=self.current_user(),video=obj))
        if purchased: self.write('yes')
        else: self.write('no')
    def post(self):
        o,t = self.request.arguments['object'][0].split(';')
        now,objs,rel = self.get_object_bydate(o,t)
        obj = globals()[objs].objects.all().filter(date=now)[0]
        pp = PlayablePurchased(owner=self.current_user(),video=obj)
        pp.save()
