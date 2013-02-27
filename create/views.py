#!/usr/bin/python
# -*- coding: utf-8 -*-
from forms import CausesForm
from models import *
from coronae import append_path
from unicodedata import normalize 
append_path()

import urllib, re

from core.stream import *
from core.social import *
from core.views import *
from spread.models import Playable

def project(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.view_project(request)

def main(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.project_form(request)
    elif request.method == 'POST':
        return proj.create_project(request)
    
def grab(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.grab_project(request)

def link_project(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.link_project(request)

def init_create(request):
    c = Create()
    if request.method == 'GET':
        return c.view_create(request)
    elif request.method == 'POST':
        return c.donate_cause(request)

def movement(request):
    group = ProjectGroup()
    if request.method == 'GET':
        return group.view_movement(request)
    elif request.method == 'POST':
        return group.create_movement(request)

class Create(Efforia):
    def __init__(self): pass
    def view_create(self, request):
        if 'object' in request.GET:
            o, t = request.GET['object'][0].split(';')
            now, objs, rel = self.get_object_bydate(o, t)
            obj = globals()[objs].objects.all().filter(date=now)
            self.get_donations(obj)
        else: return render(request, "createapp.jade", {'static_url':settings.STATIC_URL}, content_type='text/html')
    def donate_cause(self, request):
        u = self.current_user(request)
        value = int(request.POST['credits'][0])
        o, t = request.POST['object'][0].split(';')
        now, objs, rel = self.get_object_bydate(o, t)
        obj = globals()[objs].objects.all().filter(date=now)[0]
        don = CausableDonated(value=value, donator=u, cause=obj)
        don.save()
        donations = list(CausableDonated.objects.all().filter(cause=obj))
        return self.render_grid(donations, request)

class Projects(Efforia, TwitterHandler):
    def __init__(self): pass
    def project_form(self, request):
        return render(request,'project.jade',{},content_type='text/html')
    def view_project(self,request):
        ratio = sum = 0
        project_id = int(request.GET['id'])
        project = Causable.objects.filter(id=project_id)[0]
        donations = CausableDonated.objects.filter(cause=project_id)
        if len(donations) > 0:
            for d in donations: sum += d.value
            ratio = (float(sum)/float(project.credit))*100.0
        return render(request,'projectview.jade',{'project':project,'ratio':ratio},content_type='text/html')
    def create_project(self, request):
        u = self.current_user(request)
        n = t = e = ''; c = 0
        for k, v in request.POST.items():
            if 'title' in k: n = '#%s' % v.replace(" ", "")
            elif 'credit' in k: c = int(v)
            elif 'content' in k: t = v
            elif 'deadline' in k: e = datetime.strptime(v, '%d/%m/%Y')
        project = Causable(name=n, user=u, content=t, end_time=e, credit=c)
        project.save()
        self.accumulate_points(1, request)
        service = StreamService()
        access_token = u.profile.google_token
        t = re.compile(r'<.*?>').sub('', t)
        url, token = service.video_entry(n[:1], t, 'efforia', access_token)
        return render(request, 'projectvideo.jade', {'static_url':settings.STATIC_URL,
                                            'hostname':request.get_host(),
                                            'url':url, 'token':token}, content_type='text/html')
    def grab_project(self, request):
        return render(request, 'grab.jade', {}, content_type='text/html')
    def link_project(self, request):
        u = self.current_user(request)
        token = request.GET['id']
        service = StreamService()
        access_token = u.profile.google_token
        thumbnail = service.video_thumbnail(token, access_token)
        project = Causable.objects.filter(user=u).latest('date')
        project.visual = thumbnail
        project.ytoken = token
        project.save()
        self.accumulate_points(1, request)
        return redirect('/')

class ProjectGroup(Efforia):
    def __init__(self): pass
    def view_movement(self, request):
        u = self.current_user(request)
        if 'action' in request.GET:
            feed = []
            causes = Causable.objects.all().filter(user=u)
            for c in causes:
                c.name = '%s#' % c.name 
                feed.append(c)
            return self.render_grid(feed, request)
        elif 'view' in request.GET:
            move = Movement.objects.all(); feed = []; count = 0
            if 'grid' in request.GET['view']:
                for m in move.values('name').distinct():
                    feed.append(move.filter(name=m['name'], user=u)[0])
                    count += 1
            else:
                name = '#%s' % request.GET['title'].rstrip()
                for m in move.filter(name=name, user=u): feed.append(m.cause)
            return self.render_grid(feed, request)
        else: 
            move = Movement.objects.all().filter(user=u)
            message = ""
            if not len(move): message = "Você não possui nenhum movimento."
            else:
                scheds = len(Movement.objects.filter(user=u).values('name').distinct())
                message = '%i Movimentos em aberto' % scheds
            return render(request, 'movement.jade', {
                                                  'message':message,
                                                  'tutor':'Os movimentos são uma forma fácil de acompanhar todos os projetos do Efforia em que você apoia. Para utilizar, basta selecioná-los e agrupá-los num movimento.'
                                                  })
    def create_movement(self, request):
        u = self.current_user(request)
        causables = []
        objects = request.POST['objects']
        title = request.POST['title']
        objs = urllib.unquote_plus(objects).split(',')
        for o in objs: 
            ident, token = o.split(';'); token = token[:1]
            obj, rels = self.object_token(token)
            causables.append(globals()[obj].objects.filter(id=ident)[0])
        for c in causables: 
            move = Movement(user=u, cause=c, name='##' + title)
            move.save()
        self.accumulate_points(1, request)
        moves = len(Movement.objects.all().filter(user=u).values('name').distinct())
        return render(request, 'message.html', {
                                              'message':'%i Movimentos em aberto' % moves,
                                              'visual':'crowd.png',
                                              'tutor':'Os movimentos são uma forma fácil de acompanhar todos os projetos do Efforia em que você apoia. Para utilizar, basta selecioná-las e agrupá-las num movimento.'
                                              }, content_type='text/html')
