import json

from django.conf import settings
from django.http import HttpResponse as response
from django.shortcuts import render
from django.contrib.sessions.backends.cached_db import SessionStore
from pure_pagination import Paginator,PageNotAnInteger,EmptyPage
from difflib import SequenceMatcher

from models import *
from spread.models import *
from promote.models import *

def sp(x): return '!!' in x[1]
def pl(x): return '>!' in x[1]
def ev(x): return '@!' in x[1]
def im(x): return '%!' in x[1]
def ca(x): return '@#' in x[1]

class Mosaic():
    def __init__(self): pass
    def current_user(self,request):
        key = request.COOKIES['sessionid']
        s = SessionStore(key)
        session = s.load()
        if len(session): name = session['user']
        else: name = None
        user = User.objects.all().filter(username=name)
        return user[0]
    def view_mosaic(self,request,objlist=None,other=None):
        if 'user' in request.session: u = user(request.session['user'])
        else: u = user('efforia')
        try: page = request.GET.get('page',1)
        except PageNotAnInteger: page = 1
        if objlist is None: f = self.feed(u)
        else: f = objlist
        if other is None: p = u.profile
        else: p = other 
        f.sort(key=lambda item:item.date,reverse=True)
        p = Paginator(f,20,request=request)
        try: objects = p.page(page)
        except EmptyPage: return response('End of feed')
        return render(request,'grid.jade',{'f':objects,'p':p,'path':request.path,
                                           'static_url':settings.STATIC_URL},content_type='text/html')
    def verify_deadlines(self,request):
        u = self.current_user(request)
        self.verify_projects(Project.objects.filter(user=u),u)
        self.verify_videos(Playable.objects.filter(user=u),u)
        return response('Deadlines verified successfully')
    def feed(self,userobj):
        objs = json.load(open('settings.json','r'))
        feed = []; exclude = []; people = [userobj]
        for f in Followed.objects.filter(follower=userobj.id): people.append(Profile.objects.filter(id=f.followed)[0].user)
        for u in people:
            move = Movement.objects.filter(user=u)
            self.relations('Spreaded',exclude,feed,u)
            self.relations('Promoted',exclude,feed,u)
            self.group_movement(move,feed,u)
            for o in list(objs['objects']):
                e = []; objects = globals()[o].objects.filter(user=u)
                if 'Spreadable' in o: e = filter(sp,exclude)
                elif 'Playable' in o: e = filter(pl,exclude)
                elif 'Project' in o: e = filter(ca,exclude)
                elif 'Image' in o: e = filter(im,exclude)
                elif 'Event' in o: e = filter(ev,exclude)
                excludes = [x[0] for x in e]
                feed.extend(objects.exclude(id__in=excludes)) 
        return feed
    def group_movement(self,movement,feed,user):
        for v in movement.values('name').distinct():
            ts = movement.filter(name=v['name'],user=user)
            if len(ts): feed.append(ts[0])
    def relations(self,relation,exclude,feed,user):
        rels = globals()[relation].objects.filter(user=user)
        if relation is 'Spreaded':
            exclude.extend([(r.spreaded,'!!') for r in rels])
            exclude.extend([(r.spread,r.token()) for r in rels]) 
            for v in rels.values('spread').distinct():
                t = rels.filter(spread=v['spread'],user=user)
                if len(t) > 0: feed.append(t[len(t)-1])
        elif relation is 'Promoted': 
            for r in rels: 
                feed.append(r)
                exclude.append((r.prom,r.token()))
    def verify_videos(self,playables,user):
        for play in playables:
            if not play.token and not play.visual: play.delete() 
    def verify_projects(self,projects,user):
        for p in projects:
            if p.funded: continue 
            delta = p.remaining()
            # Projeto concluido, entrando para fila de movimentos
            if delta < 0:
                pledges = Pledge.objects.filter(project=p)
                move = Movement.objects.filter(cause=p)
                if len(pledges) > 0: self.verify_funding(p,pledges)
                if not p.funded:
                    if len(move) is 0: self.create_movement(p,user)
                    elif len(move) > 0: self.verify_movement(p,pledges)
            # Projeto ainda em andamento
            else: pass
    def verify_funding(self,project,pledges):
        pledge_sum = 0
        for p in pledges: pledge_sum += p.value
        if project.credit < pledge_sum:
            p = Profile.objects.filter(user_id=project.user_id)[0]
            p.credit += pledge_sum
            p.save()
            project.funded = True
            project.save()
    def verify_movement(self,project,pledges):
        elapsed = project.elapsed()
        final_d = project.deadline()+project.deadline()/2
        if elapsed > final_d:
            self.verify_funding(project,pledges)
            # Projeto nao financiado
            if not project.funded: self.return_funding(project,pledges)
    def create_movement(self,project,user):
        interests = Interest.objects.exclude(project=project).values()
        interest = Interest.objects.filter(project=project).values('key')[0]['key']
        m = Movement(name='##%s'%Interest,user=user,cause=project)
        m.save()
        for k in interests:
            s = SequenceMatcher(None,interest,k['key'])
            if s.ratio() > 0.6:
                c = Project.objects.filter(id=k['project_id'])[0]
                m = Movement(name='##%s'%interest,user=user,cause=c)
                m.save()
    def return_pledges(self,project,pledges):
        for p in pledges:
            pro = Profile.objects.filter(user_id=p.backer_id)
            pro.credit += p.value
            pro.save()
            p.delete()
        project.delete()