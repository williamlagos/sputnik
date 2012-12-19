#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from coronae import append_path
append_path()

import tornado.web,re
import simplejson as json
from tornado.web import HTTPError
from tornado import httpclient
from models import *
from datetime import datetime
from unicodedata import normalize
from core.stream import StreamService
from create.models import Causable
from core.models import Profile
from play.files import Dropbox
from core.views import *
from StringIO import StringIO

objs = json.load(open('objects.json','r'))

def upload(request):
    u = Uploads()
    if request.method == 'GET':
        return u.view_content(request)
    elif request.method == 'POST':
        return u.upload_content(request)

def collection(request):
    c = Collection()
    if request.method == 'GET':
        return c.get_quantity(request)
    elif request.method == 'POST':
        return c.view_collection(request)

def schedule(request):
    s = Schedules()
    if request.method == 'GET':
        return s.view_schedule(request)
    elif request.method == 'POST':
        return s.create_schedule(request)

class PlayHandler(Efforia):
    def get(self):
        self.srender('play.html')

class Collection(Efforia):
    def __init__(self): pass
    def get_quantity(self,request):
        u = self.current_user(request)
        count = len(Playable.objects.all().filter(user=u))+len(PlayablePurchased.objects.all().filter(owner=u))
        message = '%i Vídeos disponíveis em sua coleção para tocar.' % count
        return render(request,'collect.html',{
                                            'message':message,
                                            'visual':'collection.png',
                                            'static_url':settings.STATIC_URL,
                                            'tutor':'A coleção contempla todos os seus itens que você comprou ou assistiu, reunindo todos de uma forma prática e bem disposta.'
                                            },content_type='text/html')
    def view_collection(self,request):
        u = self.current_user(request)
        videos = list(Playable.objects.all().filter(user=u))
        videos.extend(list(PlayablePurchased.objects.all().filter(owner=u)))
        print videos
        return render(request,'grid.jade',{'f':videos,'static_url':settings.STATIC_URL},content_type='text/html')

class Uploads(Efforia):
    def __init__(self): pass
    def view_content(self,request):
        self.title = self.keys = self.text = ''
        self.category = 0
        u = self.current_user(request)
        if 'status' in request.GET:
            service = StreamService()
            status = request.GET['status']
            token = request.GET['id']
            access_token = u.profile.google_token
            thumbnail = service.video_thumbnail(token,access_token)
            play = Playable.objects.filter(user=u).latest('date')
            play.visual = thumbnail
            play.token = token
            play.save()
            self.accumulate_points(1,request)
            self.set_cookie('token',token)
            return redirect('/')
        else:
            description = ''; token = '!!'
            for k in request.GET.keys(): description += '%s;;' % request.GET[k]
            t = token.join(description[:-2].split())
            try: 
                url,token = self.parse_upload(t,request)
                return render(request,'content.html',{'static_url':settings.STATIC_URL,
                                                      'hostname':request.get_host(),
                                                      'url':url,'token':token},content_type='text/html')
            except HTTPError: return response('Não foi possível fazer o upload com estes dados. Tente outros.',content_type='text/plain') 
    def upload_content(self,request):
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
    def parse_upload(self,token,request):
        if token: content = re.split(';;',token.replace('!!',' ').replace('"',''))
        else: return response('Informação não retornada.')
        category,title,credit,text,keywords,code = content
        if 'none' in content: credit = 0
        category = int(category); keys = ','
        keywords = keywords.split(' ')
        for k in keywords: k = normalize('NFKD',k.decode('utf-8')).encode('ASCII','ignore')
        keys = keys.join(keywords)
        playable = Playable(user=self.current_user(request),name='>'+title+';'+keys,description=text,token='',category=category,credit=credit)
        playable.save()
        service = StreamService()
        access_token = self.current_user(request).profile.google_token
        return service.video_entry(title,text,keys,access_token)

class Schedules(Efforia):
    def __init__(self): pass
    def view_schedule(self,request):
        u = self.current_user(request)
        if 'action' in request.GET:
            feed = []; a = Action('selection')
            a.href = 'schedule'
            feed.append(a)
            play = Playable.objects.all().filter(user=u)
            for p in play: feed.append(p)
            return self.render_grid(feed,request)
        elif 'view' in request.GET:
            sched = Schedule.objects.all(); feed = []; count = 0
            if 'grid' in request.GET['view']:
                for m in sched.values('name').distinct():
                    if not count: 
                        a = Action('new')
                        a.href = 'schedule?action=grid'
                        feed.append(a) 
                    feed.append(sched.filter(name=m['name'],user=u)[0])
                    count += 1
            else:
                name = '>%s' % request.GET['title'].rstrip()
                feed.append(Action('play'))
                for s in sched.filter(name=name,user=u): feed.append(s.play)
            return self.render_grid(feed,request)
        else: 
            play = Schedule.objects.all().filter(user=u)
            message = ''
            if not len(play): message = "Você não possui nenhuma programação no momento. Gostaria de criar uma?"
            else:
                scheds = len(Schedule.objects.filter(user=u).values('name').distinct())
                message = '%i Programações de vídeos disponíveis' % scheds
            return render(request,'message.html',{
                                          'message':message,
                                          'visual':'schedule.png',
                                          'tutor':'As programações são uma forma fácil de acompanhar todos os vídeos do Efforia em que você assiste. Para utilizar, basta selecioná-los e agrupá-los numa programação.'
                                          },content_type='text/html')
    def create_schedule(self,request):
        u = self.current_user(request)
        playables = []
        objects = request.POST['objects']
        title = request.POST['title']
        objs = urllib.unquote_plus(str(objects)).split(',')
        for o in objs: 
            ident,token = o.split(';'); token = token[:1]
            obj,rels = self.object_token(token)
            playables.append(globals()[obj].objects.filter(id=ident)[0])
        for p in playables:
            playsched = Schedule(user=u,play=p,name='>>'+title)
            playsched.save()
        self.accumulate_points(1,request)
        scheds = len(Schedule.objects.all().filter(user=u).values('name').distinct())
        return render(request,'message.html',{
                                      'message':'%i Programações de vídeos disponíveis' % scheds,
                                      'visual':'schedule.png',
                                      'tutor':'As programações são uma forma fácil de acompanhar todos os vídeos do Efforia em que você assiste. Para utilizar, basta selecioná-los e agrupá-los numa programação.'
                                      },content_type='text/html')
    
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
