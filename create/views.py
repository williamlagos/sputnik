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

def main(request):
    proj = Project()
    if request.method == 'GET':
        return proj.view_project(request)
    elif request.method == 'POST':
        return proj.create_project(request)

def movement(request):
    group = ProjectGroup()
    if request.method == 'GET':
        return group.view_movement(request)
    elif request.method == 'POST':
        return group.create_movement(request)

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
        

class Project(Efforia,TwitterHandler):
    def __init__(self): pass
    def view_project(self,request):
        if 'view' in request.GET:
            strptime,token = request.GET['object'].split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            spreaded = globals()[rel].objects.all().filter(date=now)[0]
            feed = []; feed.append(spreaded.spreaded)
            spreads = globals()[rel].objects.all().filter(spreaded=spreaded.spreaded)
            for s in spreads: feed.append(s.spread)
            self.render_grid(feed)
        else:
            form = CausesForm()
            form.fields['title'].label = 'Título do projeto'
            form.fields['content'].initial = 'Descreva o que você pretende atingir neste projeto, de uma forma bastante breve.'
            form.fields['end_time'].label = 'Prazo final'
            return render(request,"causes.html",{'form':form},content_type='text/html')
    def create_project(self,request):
        credit = int(request.POST['credit'][0])
        token = '%s' % request.POST['token']
        name = u'%s' % request.POST['title']
        title = "#%s" % name.replace(" ","")
        text = u"%s " % request.POST["content"]
        video = Playable.objects.all().filter(token=token)[0]
        end_time = datetime.strptime(request.POST['deadline'],'%d/%m/%Y')
        cause = Causable(name='#'+name,user=self.current_user(request),play=video,content=text,end_time=end_time,credit=credit)
        cause.save()
        causes = Causable.objects.all().filter(user=self.current_user(request))
        self.accumulate_points(1,request)
        return render(request,'grid.jade',{'f':causes},content_type='text/html')

class ProjectGroup(Efforia):
    def __init__(self): pass
    def view_movement(self,request):
        u = self.current_user(request)
        if 'action' in request.GET:
            feed = []; a = Action('selection')
            a.href = 'movement'
            feed.append(a)
            causes = Causable.objects.all().filter(user=u)
            for c in causes:
                c.name = '%s#' % c.name 
                feed.append(c)
            return self.render_grid(feed,request)
        elif 'view' in request.GET:
            move = Movement.objects.all(); feed = []; count = 0
            if 'grid' in request.GET['view']:
                for m in move.values('name').distinct():
                    if not count: 
                        a = Action('new')
                        a.href = 'movement?action=grid'
                        feed.append(a)
                    feed.append(move.filter(name=m['name'],user=u)[0])
                    count += 1
            else:
                name = '#%s' % request.GET['title'].rstrip()
                feed.append(Action('play'))
                for m in move.filter(name=name,user=u): feed.append(m.cause)
            return self.render_grid(feed,request)
        else: 
            move = Movement.objects.all().filter(user=u)
            message = ""
            if not len(move): message = "Você não possui nenhum movimento. Gostaria de criar um?"
            else:
                scheds = len(Movement.objects.filter(user=u).values('name').distinct())
                message = '%i Movimentos em aberto' % scheds
            return render(request,'message.html',{
                                                  'message':message,
                                                  'visual':'crowd.png',
                                                  'tutor':'Os movimentos são uma forma fácil de acompanhar todos os projetos do Efforia em que você apoia. Para utilizar, basta selecioná-las e agrupá-las num movimento.'
                                                  })
    def create_movement(self,request):
        u = self.current_user(request)
        causables = []
        objects = request.POST['objects']
        title = request.POST['title']
        objs = urllib.unquote_plus(objects).split(',')
        for o in objs: 
            ident,token = o.split(';'); token = token[:1]
            obj,rels = self.object_token(token)
            causables.append(globals()[obj].objects.filter(id=ident)[0])
        for c in causables: 
            move = Movement(user=u,cause=c,name='##'+title)
            move.save()
        self.accumulate_points(1,request)
        moves = len(Movement.objects.all().filter(user=u).values('name').distinct())
        return render(request,'message.html',{
                                              'message':'%i Movimentos em aberto' % moves,
                                              'visual':'crowd.png',
                                              'tutor':'Os movimentos são uma forma fácil de acompanhar todos os projetos do Efforia em que você apoia. Para utilizar, basta selecioná-las e agrupá-las num movimento.'
                                              },content_type='text/html')
