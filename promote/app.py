import re,difflib
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect
from django.conf import settings

from core.main import Efforia
from core.stream import StreamService
from core.feed import Activity
from core.models import Profile
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
