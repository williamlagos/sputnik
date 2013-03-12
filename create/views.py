#!/usr/bin/python
# -*- coding: utf-8 -*-
from forms import CausesForm
from models import *
from coronae import append_path
from unicodedata import normalize 
append_path()

import urllib,re,random

from core.stream import *
from core.social import *
from core.views import *

def project(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.view_project(request)
    
def movements(request):
    group = ProjectGroup()
    if request.method == 'GET':
        return group.movement_form(request)

def promote(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.promote_form(request)
    elif request.method == 'POST':
        return proj.promote_project(request)

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

def pledge(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.view_pledge(request)
    elif request.method == 'POST':
        return proj.pledge_project(request)

def link(request):
    proj = Projects()
    if request.method == 'GET':
        return proj.link_project(request)

def init_create(request):
    c = Create()
    if request.method == 'GET':
        return c.view_create(request)

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

class Projects(Efforia, TwitterHandler):
    def __init__(self): pass
    def project_form(self, request):
        return render(request,'project.jade',{},content_type='text/html')
    def view_project(self,request):
        ratio = sum = 0; backers = set([])
        project_id = int(request.GET['id'])
        project = Causable.objects.filter(id=project_id)[0]
        pledges = Pledge.objects.filter(project_id=project_id)
        if len(pledges) > 0:
            for d in pledges:
                backers.add(d.backer) 
                sum += d.value
            ratio = (float(sum)/float(project.credit))*100.0
        remaining = abs(project.remaining())
        backers = len(backers)
        return render(request,'projectview.jade',{
                                                  'project':project,
                                                  'ratio':ratio,
                                                  'remaining':remaining,
                                                  'backers':backers},content_type='text/html')
    def create_project(self, request):
        u = self.current_user(request)
        n = t = e = key = ''; c = 0
        for k, v in request.POST.items():
            if 'title' in k: n = '#%s' % v.replace(" ", "")
            elif 'credit' in k: c = int(v)
            elif 'content' in k: t = v
            elif 'deadline' in k: e = datetime.strptime(v, '%d/%m/%Y')
            elif 'keyword' in k: key = v
        project = Causable(name=n,user=u,content=t,end_time=e,credit=c)
        project.save()
        keyword = Keyword(project=project,key=key)
        keyword.save()
        self.accumulate_points(1, request)
        service = StreamService()
        access_token = u.profile.google_token
        t = re.compile(r'<.*?>').sub('', t)
        url, token = service.video_entry(n[:1], t, 'efforia', access_token)
        return render(request, 'projectvideo.jade', {'static_url':settings.STATIC_URL,
                                            'hostname':request.get_host(),
                                            'url':url, 'token':token}, content_type='text/html')
    def view_pledge(self,request):
        return render(request,'pledge.jade',{},content_type='text/html')
    def pledge_project(self,request):
        u = self.current_user(request)
        value = int(request.POST['credits'])
        prjid = request.POST['object']
        project = Causable.objects.filter(id=prjid)[0]
        don = Pledge(value=value,backer=u,project=project)
        don.save()
        # Código para obter lista de apoiadores
        # donations = list(Pledge.objects.all().filter(project=obj))
        return response('Pledge created successfully.')
    def grab_project(self, request):
        profile = self.current_user(request).profile
        return render(request,'grab.jade',{'credit':profile.credit},content_type='text/html')
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
    def promote_form(self,request):
        return render(request,'promote.jade',{},content_type='text/html')
    def promote_project(self,request):
        u = self.current_user(request)
        c = request.POST['content']
        objid = request.POST['id']
        token = request.POST['token']
        move = Movement.objects.filter(cause_id=objid)
        if len(move) > 0: p = Promoted(name='$#',prom=objid,content=c,user=u); p.save()
        else: s = Promoted(name=token,prom=objid,content=c,user=u); s.save() 
        return response('Project promoted successfully')

class ProjectGroup(Efforia):
    def __init__(self): pass
    def movement_form(self,request):
        keywords = []
        for key in Keyword.objects.all().values('key'): 
            keywords.append(key['key'])
        random.shuffle(keywords) 
        return render(request,'movement.jade',{'keys':keywords[:10],'quantity':len(keywords)},content_type='text/html')
#        ; message = ""
#        move = Movement.objects.all().filter(user=u)
#        if not len(move): message = "Você não possui nenhum movimento."
#        else:
#            scheds = len(Movement.objects.filter(user=u).values('name').distinct())
#            message = '%i Movimentos em aberto' % scheds
#        return render(request, 'movement.jade', {
#                                              'message':message,
#                                              })
    def select_project(self,request):
        u = self.current_user(request); feed = []
        causes = Causable.objects.all().filter(user=u)
        for c in causes:
            c.name = '%s#' % c.name 
            feed.append(c)
        return self.render_grid(feed,request)
    def view_movement(self,request):
        u = self.current_user(request)
        move = Movement.objects.all(); feed = []; count = 0
        name = '#%s' % request.GET['title'].rstrip()
        for m in move.filter(name=name,user=u): feed.append(m.cause)
        return self.render_grid(feed,request)
    def create_movement(self,request):
        u = self.current_user(request)
        title = request.POST['title']
        key = request.POST['interest']
        p = Keyword.objects.filter(key=key)[0].project
        keywords = Keyword.objects.exclude(project=p).values()
        keyword = Keyword.objects.filter(project=p).values('key')[0]['key']
        m = Movement(name='##%s'%title,user=u,cause=p)
        m.save()
        for k in keywords:
            s = SequenceMatcher(None,keyword,k['key'])
            if s.ratio() > 0.6:
                c = Causable.objects.filter(id=k['project_id'])[0]
                m = Movement(name='##%s'%title,user=u,cause=c)
                m.save()
        return response('Movement created successfully')
