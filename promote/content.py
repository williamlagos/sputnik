import random
from difflib import SequenceMatcher
from django.shortcuts import render
from django.http import HttpResponse as response

from core.main import Efforia
from models import Interest,Movement,Project

class Movements(Efforia):
    def __init__(self): pass
    def movement_form(self,request):
        Interests = []
        for key in Interest.objects.all().values('key'): 
            Interests.append(key['key'])
        random.shuffle(Interests) 
        return render(request,'movement.jade',{'keys':Interests[:10],'quantity':len(Interests)},content_type='text/html')
    def view_movement(self,request):
        u = self.current_user(request)
        move = Movement.objects.all(); feed = []; count = 0
        name = '##%s' % request.GET['title'].rstrip()
        for m in move.filter(name=name,user=u): feed.append(m.cause)
        return self.view_mosaic(request,feed)
    def create_movement(self,request):
        u = self.current_user(request)
        title = request.POST['title']
        key = request.POST['interest']
        p = Interest.objects.filter(key=key)[0].project
        interests = Interest.objects.exclude(project=p).values()
        interest = Interest.objects.filter(project=p).values('key')[0]['key']
        m = Movement(name='##%s'%title,user=u,cause=p)
        m.save()
        for k in interests:
            s = SequenceMatcher(None,interest,k['key'])
            if s.ratio() > 0.6:
                c = Project.objects.filter(id=k['project_id'])[0]
                m = Movement(name='##%s'%title,user=u,cause=c)
                m.save()
        return response('Movement created successfully')
