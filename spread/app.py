import re
from unicodedata import normalize
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect
from django.conf import settings

from models import Spreadable,Image,Playable
from core.models import Profile
from core.files import Dropbox
from core.stream import StreamService
from core.main import Efforia

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
        res = self.url_request(link)
        url = '%s?dl=1' % res
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
            r = redirect('/')
            r.set_cookie('token',token)
            return r
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
