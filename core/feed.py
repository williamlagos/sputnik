import json

from django.conf import settings
from django.http import HttpResponse as response
from django.shortcuts import render
from pure_pagination import Paginator,PageNotAnInteger,EmptyPage
from difflib import SequenceMatcher
from coronae import Coronae

from models import *
from spread.models import *
from create.models import *

class Mosaic(Coronae):
    def __init__(self): pass
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
        self.verify_projects(Causable.objects.filter(user=u),u)
        self.verify_videos(Playable.objects.filter(user=u),u)
        return response('Deadlines verified successfully')
    def feed(self,userobj):
        objs = json.load(open('objects.json','r'))
        feed = []; exclude = []; people = [userobj]
        for f in Followed.objects.filter(follower=userobj.id): people.append(Profile.objects.filter(id=f.followed)[0].user)
        for u in people:
            self.relations('Spreaded',exclude,feed,u)
            self.relations('Promoted',exclude,feed,u)
            for o in objs['objects'].values():
                types = globals()[o].objects.all()
                if 'Movement' in o: self.group_movement(types,feed,u)
                elif 'Playable' in o or 'Image' in o or 'Spreadable' in o or 'Causable' in o or 'Event' in o:
                    relations = types.filter(user=u)
                    for r in relations:
                        object_id = int(r.id)
                        if object_id not in exclude: feed.append(r)
                else: feed.extend(types.filter(user=u))
        return feed
    def group_movement(self,movement,feed,user=None):
        for v in movement.values('name').distinct():
            if user is not None: ts = movement.filter(name=v['name'],user=user)
            else: ts = movement.filter(name=v['name'])
            if len(ts): feed.append(ts[0])
    def relations(self,relation,exclude,feed,user):
        rels = globals()[relation].objects.all().filter(user=user)
        if relation is 'Spreaded':
            for r in rels:
                exclude.append(r.spreaded)                            
                exclude.append(r.spread)
            for v in rels.values('spread').distinct():
                ts = rels.filter(spread=v['spread'],user=user)
                if len(ts): feed.append(ts[len(ts)-1])
        elif relation is 'Promoted': 
            for r in rels:
                exclude.append(r.prom)
                feed.append(r)
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
        keywords = Keyword.objects.exclude(project=project).values()
        keyword = Keyword.objects.filter(project=project).values('key')[0]['key']
        m = Movement(name='##%s'%keyword,user=user,cause=project)
        m.save()
        for k in keywords:
            s = SequenceMatcher(None,keyword,k['key'])
            if s.ratio() > 0.6:
                c = Causable.objects.filter(id=k['project_id'])[0]
                m = Movement(name='##%s'%keyword,user=user,cause=c)
                m.save()
    def return_pledges(self,project,pledges):
        for p in pledges:
            pro = Profile.objects.filter(user_id=p.backer_id)
            pro.credit += p.value
            pro.save()
            p.delete()
        project.delete()