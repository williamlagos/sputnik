import re,difflib
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect
from django.conf import settings

from efforia.main import Efforia
from efforia.stream import StreamService
from efforia.feed import Activity
from efforia.models import Profile
from models import Event,Pledge,Project,Interest,Movement,Promoted

def ca(x): return '@#' in x[1]
def ev(x): return '@!' in x[1]

class Application(Activity):
    def __init__(self,user,app):
        Activity.__init__(self,user,app)
    def deadline(self):
        projects = Project.objects.filter(user=self.user)
        for p in projects:
            if p.funded: continue 
            delta = p.remaining()
            # Projeto concluido, entrando para fila de movimentos
            if delta < 0:
                pledges = Pledge.objects.filter(project=p)
                move = Movement.objects.filter(cause=p)
                if len(pledges) > 0: self.verify_funding(p,pledges)
                if not p.funded:
                    if len(move) is 0: self.create_movement(p)
                    elif len(move) > 0: self.verify_movement(p,pledges)
            # Projeto ainda em andamento
            else: pass
    def relations(self,feed):
        excludes = []; rels = Promoted.objects.filter(user=self.user)
        for r in rels: feed.append(r); excludes.append((r.prom,r.token()))
        return excludes
    def groupables(self,feed):
        movement = Movement.objects.filter(user=self.user)
        for v in movement.values('name').distinct():
            ts = movement.filter(name=v['name'],user=self.user)
            if len(ts): feed.append(ts[0])
    def duplicates(self,exclude,feed):
        for o in self.objects:
            objects = globals()[o].objects.filter(user=self.user)
            if 'Project' in o: e = filter(ca,exclude)
            elif 'Event' in o: e = filter(ev,exclude)
            excludes = [x[0] for x in e]
            feed.extend(objects.exclude(id__in=excludes))
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
        m = Movement(name='##%s'%interest,user=user,cause=project)
        m.save()
        for k in interests:
            s = difflib.SequenceMatcher(None,interest,k['key'])
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
