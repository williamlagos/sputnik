import random
from difflib import SequenceMatcher
from django.shortcuts import render
from django.http import HttpResponse as response

from efforia.main import Efforia
from models import Interest,Movement,Project

class Projects(Efforia):
    def __init__(self): pass
    def start_promoteapp(self, request):
        return render(request, "createapp.jade", {'static_url':settings.STATIC_URL}, content_type='text/html')
    def project_form(self, request):
        return render(request,'project.jade',{},content_type='text/html')
    def view_backers(self,request):
        backers = []; u = self.current_user(request)
        pledge = Pledge.objects.filter(project_id=request.GET['project_id'])
        for p in pledge: backers.append(p.backer.profile)
        return self.view_mosaic(request,backers)
    def view_project(self,request):
        ratio = sum = 0; backers = set([])
        project_id = int(request.GET['id'])
        project = Project.objects.filter(id=project_id)[0]
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
        project = Project(name=n,user=u,content=t,end_time=e,credit=c)
        project.save()
        interest = Interest(project=project,key=key)
        interest.save()
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
        project = Project.objects.filter(id=prjid)[0]
        don = Pledge(value=value,backer=u,project=project)
        don.save()
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
        project = Project.objects.filter(user=u).latest('date')
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
