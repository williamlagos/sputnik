import re
from unicodedata import normalize
from datetime import datetime,time
from django.shortcuts import render
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect
from django.conf import settings

from models import Page,Event,Spreadable,Image,Playable
from core.models import Profile
from core.files import Dropbox
from core.stream import StreamService
from core.main import Efforia

class Pages(Efforia):
    def __init__(self): pass
    def view_page(self,request):
        return render(request,'page.jade',{},content_type='text/html')
    def create_page(self,request):
        print request.POST
        c = request.POST['content']
        t = request.POST['title']
        u = self.current_user(request)
        p = Page(content=c,user=u,name='!#%s' % t)
        p.save()
        return render(request,'pageview.jade',{'content':c},content_type='text/html')
    def edit_page(self,request):
        page_id = int(request.GET['id'])
        p = Page.objects.filter(id=page_id)[0]
        return render(request,'pagedit.jade',{
                       'title':p.name,
                       'content':p.content.encode('utf-8'),
                       'pageid':page_id},content_type='text/html')
    def save_page(self,request):
        page_id = request.POST['id']
        p = Page.objects.filter(id=page_id)[0]
        for k,v in request.POST.items():
            if 'content' in k:
                if len(v) > 0: p.content = v
            elif 'title' in k:
                if len(v) > 0: p.name = v
        p.save()
        return response('Page saved successfully')
    def page_view(self,request):
        n = request.GET['title']
        c = Page.objects.filter(name=n)[0].content
        return render(request,'pageview.jade',{'content':c},content_type='text/html')

class Images(Efforia):
    def __init__(self): pass
    def view_image(self,request):
        return render(request,'image.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
    def create_image(self,request):
        u = self.current_user(request)
        if 'description' in request.POST:
            image = list(Image.objects.filter(user=u))[-1:][0]
            descr = request.POST['description']
            image.description = descr
            image.save()
            return response('Description added to image successfully')
        photo = request.FILES['Filedata'].read()
        dropbox = Dropbox()
        link = dropbox.upload_and_share(photo)
        res = self.do_request(link)
        url = '%s?dl=1' % res.effective_url
        i = Image(link=url,user=u)
        i.save()
        return response('Image created successfully')

class Spreads(Efforia):
    def __init__(self): pass
    def start_spreadapp(self,request):
        return render(request,'spreadapp.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
    def view_spread(self,request):
        return render(request,"spread.jade",{},content_type='text/html')
    def create_spread(self,request):
        u = self.current_user(request)
        name = u.first_name.lower()
        text = unicode('%s' % (request.POST['content']))
        post = Spreadable(user=u,content=text,name='!'+name)
        post.save()
        self.accumulate_points(1,request)
        return response('Spreadable created successfully')
    
class Events(Efforia):
    def __init__(self): pass
    def view_event(self,request):
        return render(request,'event.jade',{},content_type='text/html')
    def create_event(self,request):
        name = request.POST['name']
        local = request.POST['location']
        times = request.POST['start_time'],request.POST['end_time']
        dates = []
        for t in times: 
            strp_time = time.strptime(t,'%d/%m/%Y')
            dates.append(datetime.fromtimestamp(time.mktime(strp_time)))
        event_obj = Event(name='@@'+name,user=self.current_user(request),start_time=dates[0],
                          end_time=dates[1],location=local,id_event='',rsvp_status='')
        event_obj.save()
        self.accumulate_points(1,request)
        return response('Event created successfully')

class Uploads(Efforia):
    def __init__(self): pass
    def view_upload(self,request):
        return render(request,'content.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
    def view_content(self,request):
        self.title = self.keys = self.text = ''
        self.category = 0
        u = self.current_user(request)
        if 'status' in request.GET:
            service = StreamService()
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
                return render(request,'video.jade',{'static_url':settings.STATIC_URL,
                                                      'hostname':request.get_host(),
                                                      'url':url,'token':token},content_type='text/html')
            except Exception: return response('Invalid file for uploading') 
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
        else: return response('Information not returned')
        category,title,text,credit,keywords = content[:-1]
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
    
#class Purchases(Efforia):
#    def __init__(self): pass
#    def verify_purchased(self,request):
#        u = self.current_user(request)
#        o,t = request.GET['object'].split(';')
#        now,objs,rel = self.get_object_bydate(o,t)
#        obj = globals()[objs].objects.all().filter(date=now)[0]
#        purchased = len(PlayablePurchased.objects.all().filter(owner=u,video=obj))
#        if purchased: return response('yes')
#        else: return response('no')
#    def purchase_video(self,request):
#        u = self.current_user(request)
#        o,t = request.POST['object'].split(';')
#        now,objs,rel = self.get_object_bydate(o,t)
#        obj = globals()[objs].objects.all().filter(date=now)[0]
#        pp = PlayablePurchased(owner=u,video=obj)
#        pp.save()
#        return response('Video purchased.')