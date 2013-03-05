#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,re
from datetime import datetime,date
from unicodedata import normalize
from StringIO import StringIO

from django.contrib.auth.models import User
from django.utils.html import escape
from django.conf import settings
from django.shortcuts import render,redirect

from tornado.auth import FacebookGraphMixin
from tornado import httpclient
import json

from core.stream import *
from core.social import *
from core.models import *
from core.forms import *
from core.views import *
from core.views import *

from create.models import Causable

from forms import *
from models import *
from files import Dropbox

from coronae import Coronae,append_path

append_path()

objs = json.load(open('objects.json','r'))

def spreadspread(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.spreadspread(request)
    elif request.method == 'POST':
        return s.spreadobject(request)

def pageview(request):
    p = PageView()
    if request.method == 'GET':
        return p.view_page(request)
    
def pageedit(request):
    p = Pages()
    if request.method == 'GET':
        return p.edit_page(request)
    elif request.method == 'POST':
        return p.save_page(request)

def spreadable(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_spreadable(request)
    
def playable(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_playable(request)

def eventview(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_event(request)

def imageview(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_images(request)

def page(request):
    p = Pages()
    if request.method == 'GET':
        return p.view_page(request)
    elif request.method == 'POST':
        return p.create_page(request)

def image(request):
    i = Images()
    if request.method == 'GET':
        return i.view_image(request)
    elif request.method == 'POST':
        return i.create_image(request)
    
def upload(request):
    u = Uploads()
    if request.method == 'GET':
        return u.view_content(request)
    elif request.method == 'POST':
        return u.upload_content(request)

def collection(request):
    c = Collection()
    if request.method == 'GET':
        return c.get_quantity(request)
    elif request.method == 'POST':
        return c.view_collection(request)

def schedule(request):
    s = Schedules()
    if request.method == 'GET':
        return s.view_schedule(request)
    elif request.method == 'POST':
        return s.create_schedule(request)

def purchase(request):
    p = Purchases()
    if request.method == 'GET':
        return p.verify_purchased(request)
    elif request.method == 'POST':
        return p.purchase_video(request)

def init_spread(request):
    return render(request,'spreadapp.jade',{'static_url':settings.STATIC_URL},content_type='text/html')    

def main(request):
    graph = SocialGraph()
    if request.method == 'GET': 
        return graph.view_spread(request)
    elif request.method == 'POST': 
        return graph.create_spread(request)
    
def event(request):
    graph = SocialGraph()
    if request.method == 'GET':
        return graph.view_event(request)
    elif request.method == 'POST':
        return graph.create_event(request)

def content(request):
    return render(request,'content.jade',{'static_url':settings.STATIC_URL},content_type='text/html')

class Spreadables(Efforia):
    def __init__(self): pass
    def view_spreadable(self,request):
        spread_id = int(request.GET['id'])
        s = Spreadable.objects.filter(id=spread_id)[0]
        return render(request,'spreadview.jade',{'content':s.content,'spreadid':spread_id},content_type='text/html')
    def view_event(self,request):
        event_id = int(request.GET['id'])
        e = Event.objects.filter(id=event_id)[0]
        return render(request,'eventview.jade',{'title':e.name,'location':e.location,'eventid':event_id},content_type='text/html')
    def view_playable(self,request):
        playable_id = int(request.GET['id'])
        e = Playable.objects.filter(id=playable_id)[0]
        return render(request,'videoview.jade',{'playableid':playable_id},content_type='text/html')
    def view_images(self,request):
        image_id = int(request.GET['id'])
        i = Image.objects.filter(id=image_id)[0]
        return render(request,'imageview.jade',{'image':i.link,'imageid':image_id},content_type='text/html')
    def spreadspread(self,request):
        return render(request,'spread.jade',{'id':request.GET['id']},content_type='text/html')
    def spreadobject(self,request):
        oid = request.GET['id']
        obj = self.object_token(request.GET['token'])[0]
        query = globals()[obj].objects.filter(id=oid)
        return response('Hello World!')

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

class PageView(Efforia):
    def __init__(self): pass
    def view_page(self,request):
        n = request.GET['title']
        c = Page.objects.filter(name=n)[0].content
        return render(request,'pageview.jade',{'content':c},content_type='text/html')

class Images(Efforia):
    def __init__(self): pass
    def view_image(self,request):
        return render(request,'image.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
    def create_image(self,request):
        photo = request.FILES['Filedata'].read()
        dropbox = Dropbox()
        link = dropbox.upload_and_share(photo)
        client = httpclient.HTTPClient()
        response = client.fetch(link)
        url = '%s?dl=1' % response.effective_url
        i = Image(link=url,user=self.current_user(request))
        i.save()
        imgs = Image.objects.filter(user=self.current_user(request))
        return render(request,'grid.jade',{'f':imgs},content_type='text/html')

class Social(Efforia):
    def __init__(self): pass
    def view_spread(self,request):
        if 'view' in request.GET:
            strptime,token = request.GET['object'].split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            spreaded = globals()[rel].objects.all().filter(date=now)[0]
            feed = []; feed.append(spreaded.spreaded)
            spreads = globals()[rel].objects.all().filter(spreaded=spreaded.spreaded)
            for s in spreads: feed.append(s.spread)
            self.render_grid(feed)
        else:
            return render(request,"spread.jade",{},content_type='text/html')
    def create_spread(self,request):
        u = self.current_user(request)
        if 'spread' in request.POST:
            c = request.POST['spread'][0]
            spread = Spreadable(user=u,content=c,name='!'+u.username)
            spread.save()
            strptime,token = request.POST['time'][0].split(';')
            now,objs,rels = self.get_object_bydate(strptime,token)
            o = globals()[objs].objects.all().filter(date=now)[0]
            relation = globals()[rels](spreaded=o,spread=spread,user=u)
            relation.save()
            spreads = []; spreads.append(o)
            spreadablespreads = globals()[rels].objects.all().filter(spreaded=o,user=u)
            for s in spreadablespreads: spreads.append(s.spread)
        else:
            spread = self.spread_post(request)
            spread.save()
            spreads = Spreadable.objects.all().filter(user=u)
        feed = []
        self.accumulate_points(1,request)
        for s in spreads: feed.append(s)
        feed.sort(key=lambda item:item.date,reverse=True)
        return self.render_grid(feed,request)
    def spread_post(self,request):
        print request.POST
        name = self.current_user(request).first_name.lower()
        text = unicode('%s !%s' % (request.POST['content'],name))
        user = self.current_user(request)
        post = Spreadable(user=user,content=text,name='!'+name)
        return post
    
class SocialGraph(Social,FacebookGraphMixin):
    def __init__(self): pass
    def view_event(self,request):
        if 'view' in request.GET:
            strptime,token = request.GET['object'].split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            spreaded = globals()[rel].objects.all().filter(date=now)[0]
            feed = []; feed.append(spreaded.spreaded)
            spreads = globals()[rel].objects.all().filter(spreaded=spreaded.spreaded)
            for s in spreads: feed.append(s.spread)
            self.render_grid(feed)
        else:
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
        events = Event.objects.all().filter(user=self.current_user(request))
        return render(request,'grid.jade',{'f':events},content_type='text/html')

class Register(Coronae,GoogleHandler,TwitterHandler,FacebookHandler,tornado.auth.TwitterMixin,tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        google_id = self.get_argument("google_id",None)
        google = self.get_argument("google_token",None)
        twitter_id = self.get_argument("twitter_id",None)
        twitter = self.get_argument("twitter_token",None)
        facebook = self.get_argument("facebook_token",None)
        self.google_token = self.twitter_token = self.facebook_token = response = ''
        google = 'empty' if not google else google
        if 'empty' not in google:
            if self.get_current_user():
                profile = Profile.objects.all().filter(user=self.current_user())[0]
                profile.google_token = google
                profile.save()
                self.redirect('/')
            else:
                if len(User.objects.all().filter(username=google_id)) > 0: return
                profile = self.google_credentials(google)
                profile['google_token'] = google
                self.google_enter(profile,False)
        if google_id:
            user = User.objects.all().filter(username=google_id)
            if len(user) > 0:
                token = user[0].profile.google_token
                profile = self.google_credentials(token) 
                self.google_enter(profile)
            else:
                self.approval_prompt()
        if twitter:
            user = User.objects.all().filter(username=twitter_id)
            prof = ast.literal_eval(str(twitter))
            if len(user) > 0: self.twitter_enter(prof)
            elif not self.get_current_user():
                self.twitter_token = prof 
                self.twitter_credentials(twitter)
            else:
                profile = Profile.objects.all().filter(user=self.current_user())[0]
                profile.twitter_token = prof['key']+';'+prof['secret']
                profile.save()
                self.redirect('/')
        elif facebook: 
            prof = Profile.objects.all().filter(facebook_token=facebook)
            if len(prof) > 0: self.facebook_token = self.facebook_credentials(facebook)
            elif not self.get_current_user(): self.facebook_token = self.facebook_credentials(facebook)
            else:
                profile = Profile.objects.all().filter(user=self.current_user())[0]
                profile.facebook_token = facebook
                profile.save()
                self.redirect('/')
        else:
            self._on_response(response)
    def google_enter(self,profile,exist=True):
        if not exist:
            age = date.today()
            contact = profile['link'] if 'link' in profile else ''
            data = {
                    'username':     profile['id'],
                    'first_name':   profile['given_name'],
                    'last_name':    profile['family_name'],
                    'email':        contact,
                    'google_token': profile['google_token'],
                    'password':     '3ff0r14',
                    'age':          age        
            }
            self.create_user(data)
        self.login_user(profile['id'],'3ff0r14')
    def twitter_enter(self,profile,exist=True):
        if not exist:
            age = date.today()
            names = profile['name'].split()[:2]
            given_name,family_name = names if len(names) > 1 else (names[0],'')
            data = {
                    'username':     profile['user_id'],
                    'first_name':   given_name,
                    'last_name':    family_name,
                    'email':        '@'+profile['screen_name'],
                    'twitter_token': profile['key']+';'+profile['secret'],
                    'password':     '3ff0r14',
                    'age':          age        
            }
            self.create_user(data)
        self.login_user(profile['user_id'],'3ff0r14')
    def facebook_enter(self,profile,exist=True):
        if not exist:
            strp_time = time.strptime(profile['birthday'],"%m/%d/%Y")
            age = datetime.fromtimestamp(time.mktime(strp_time))
            if 'first_name' not in profile:
                names = profile['name'].split()[:2]
                profile['first_name'],profile['last_name'] = names if len(names) > 1 else (names[0],'')
            data = {
                'username':   profile['id'],
                'first_name': profile['first_name'],
                'last_name':  profile['last_name'],
                'email':      profile['link'],
                'facebook_token': self.facebook_token,
                'password':   '3ff0r14',
                'age':        age
            }
            self.create_user(data)
        self.login_user(profile['id'],'3ff0r14')
    def _on_twitter_response(self,response):
        if response is '': return
        profile = self.twitter_token
        prof = ast.literal_eval(str(response))
        profile['name'] = prof['name']
        self.twitter_enter(profile,False)
    def _on_facebook_response(self,response):
        if response is '': return
        profile = ast.literal_eval(str(response))
        print profile
        user = User.objects.all().filter(username=profile['id'])
        if len(user) > 0: self.facebook_enter(profile)
        else: self.facebook_enter(profile,False)
    def _on_response(self,response):
        form = RegisterForm()
        return self.render(self.templates()+"simpleform.html",form=form,submit='Entrar',action='register')
    @tornado.web.asynchronous
    def post(self):
        data = {
            'username':self.request.arguments['username'][0],
            'email':self.request.arguments['email'][0],
            'password':self.request.arguments['password'][0],
            'last_name':self.request.arguments['last_name'][0],
            'first_name':self.request.arguments['first_name'][0]
        }
        form = RegisterForm(data=data)
        if len(User.objects.filter(username=self.request.arguments['username'][0])) < 1:
            strp_time = time.strptime(self.request.arguments['birthday'][0],"%m/%d/%Y")
            birthday = datetime.fromtimestamp(time.mktime(strp_time)) 
            form.data['age'] = birthday
            self.create_user(form.data)
        username = self.request.arguments['username'][0]
        password = self.request.arguments['password'][0]
        self.login_user(username,password)
    def create_user(self,data):
        user = User.objects.create_user(data['username'],
                                        data['email'],
                                        data['password'])
        user.last_name = data['last_name']
        user.first_name = data['first_name']
        user.save()
        google_token = twitter_token = facebook_token = ''
        if 'google_token' in data: google_token = data['google_token']
        elif 'twitter_token' in data: twitter_token = data['twitter_token']
        elif 'facebook_token' in data: facebook_token = data['facebook_token']
        profile = Profile(user=user,birthday=data['age'],
                          twitter_token=twitter_token,
                          facebook_token=facebook_token,
                          google_token=google_token)
        profile.save()
    def login_user(self,username,password):
        auth = self.authenticate(username,password)
        if auth is not None:
            self.set_cookie("user",tornado.escape.json_encode(username))
            self.redirect("/")
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Falha no login")
            self.redirect(u"/login" + error_msg)
    def authenticate(self,username,password):
        # TODO: Fazer o login funcionar normalmente pelas redes sociais.
        exists = User.objects.filter(username=username)
        if exists:
            if exists[0].check_password(password):
                return 1
        else: return None

class TwitterPosts(Coronae,TwitterHandler):
    def get(self):
        name = self.current_user().username
        text = unicode('%s !%s' % (self.request.arguments['content'][0],name))
        limit = 135-len(name)
        if len(self.request.arguments['content']) > limit: 
            short = unicode('%s... !%s' % (self.request.arguments['content'][0][:limit],name))
        else: short = text
        twitter = self.current_user().profile.twitter_token
        if not twitter: twitter = get_offline_access()['twitter_token']
        access_token = self.format_token(twitter)
        encoded = short.encode('utf-8')
        self.twitter_request(
            "/statuses/update",
            post_args={"status": encoded},
            access_token=access_token,
            callback=self.async_callback(self.posted))
        self.write('Postagem tuitada com sucesso.')
    def posted(self,response): pass

class FacebookPosts(Coronae,FacebookHandler):
    def get(self):
        facebook = self.current_user().profile.facebook_token
        if facebook:
            name = self.current_user().username
            text = unicode('%s !%s' % (self.request.arguments['content'],name))
            encoded_facebook = text.encode('utf-8')
            self.facebook_request("/me/feed",post_args={"message": encoded_facebook},
                              access_token=facebook,
                              callback=self.async_callback(self.posted))
            self.write('Postagem publicada com sucesso.')
    def posted(self,response): pass
    
class FacebookEvents(Coronae,FacebookHandler):
    def get(self):
        name = self.request.arguments['name'][0]
        times = self.request.arguments['start_time'][0],self.request.arguments['end_time'][0]
        dates = []
        for t in times: 
            strp_time = time.strptime(t,'%d/%m/%Y')
            dates.append(datetime.fromtimestamp(time.mktime(strp_time)))
        facebook = self.current_user().profile.facebook_token
        if facebook:
            args = { 'name':name, 'start_time':dates[0], 'end_time':dates[1] }
            self.facebook_request("/me/events",access_token=facebook,post_args=args,
                                  callback=self.async_callback(self.posted))
    def posted(self): pass

class Collection(Efforia):
    def __init__(self): pass
    def get_quantity(self,request):
        u = self.current_user(request)
        count = len(Playable.objects.all().filter(user=u))+len(PlayablePurchased.objects.all().filter(owner=u))
        message = '%i Vídeos disponíveis em sua coleção para tocar.' % count
        return render(request,'collect.html',{
                                            'message':message,
                                            'visual':'collection.png',
                                            'static_url':settings.STATIC_URL,
                                            'tutor':'A coleção contempla todos os seus itens que você comprou ou assistiu, reunindo todos de uma forma prática e bem disposta.'
                                            },content_type='text/html')
    def view_collection(self,request):
        u = self.current_user(request)
        videos = list(Playable.objects.all().filter(user=u))
        videos.extend(list(PlayablePurchased.objects.all().filter(owner=u)))
        print videos
        return render(request,'grid.jade',{'f':videos,'static_url':settings.STATIC_URL},content_type='text/html')

class Uploads(Efforia):
    def __init__(self): pass
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
            except HTTPError: return response('Não foi possível fazer o upload com estes dados. Tente outros.',content_type='text/plain') 
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
        else: return response('Informação não retornada.')
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

class Schedules(Efforia):
    def __init__(self): pass
    def view_schedule(self,request):
        u = self.current_user(request)
        if 'action' in request.GET:
            feed = []; a = Action('selection')
            a.href = 'schedule'
            feed.append(a)
            play = Playable.objects.all().filter(user=u)
            for p in play: feed.append(p)
            return self.render_grid(feed,request)
        elif 'view' in request.GET:
            sched = Schedule.objects.all(); feed = []; count = 0
            if 'grid' in request.GET['view']:
                for m in sched.values('name').distinct():
                    if not count: 
                        a = Action('new')
                        a.href = 'schedule?action=grid'
                        feed.append(a) 
                    feed.append(sched.filter(name=m['name'],user=u)[0])
                    count += 1
            else:
                name = '>%s' % request.GET['title'].rstrip()
                feed.append(Action('play'))
                for s in sched.filter(name=name,user=u): feed.append(s.play)
            return self.render_grid(feed,request)
        else: 
            play = Schedule.objects.all().filter(user=u)
            message = ''
            if not len(play): message = "Você não possui nenhuma lista no momento. Gostaria de criar uma?"
            else:
                scheds = len(Schedule.objects.filter(user=u).values('name').distinct())
                message = '%i Programações de vídeos disponíveis' % scheds
            return render(request,'schedule.jade',{
                                          'message':message,
                                          'tutor':'As listas são uma forma fácil de acompanhar todos os vídeos do Efforia em que você assiste. Para utilizar, basta selecioná-los e agrupá-los numa programação.'
                                          },content_type='text/html')
    def create_schedule(self,request):
        u = self.current_user(request)
        playables = []
        objects = request.POST['objects']
        title = request.POST['title']
        objs = urllib.unquote_plus(str(objects)).split(',')
        for o in objs: 
            ident,token = o.split(';'); token = token[:1]
            obj,rels = self.object_token(token)
            playables.append(globals()[obj].objects.filter(id=ident)[0])
        for p in playables:
            playsched = Schedule(user=u,play=p,name='>>'+title)
            playsched.save()
        self.accumulate_points(1,request)
        scheds = len(Schedule.objects.all().filter(user=u).values('name').distinct())
        return render(request,'message.html',{
                                      'message':'%i Programações de vídeos disponíveis' % scheds,
                                      'visual':'schedule.png',
                                      'tutor':'As programações são uma forma fácil de acompanhar todos os vídeos do Efforia em que você assiste. Para utilizar, basta selecioná-los e agrupá-los numa programação.'
                                      },content_type='text/html')
    
class Purchases(Efforia):
    def __init__(self): pass
    def verify_purchased(self,request):
        u = self.current_user(request)
        o,t = request.GET['object'].split(';')
        now,objs,rel = self.get_object_bydate(o,t)
        obj = globals()[objs].objects.all().filter(date=now)[0]
        purchased = len(PlayablePurchased.objects.all().filter(owner=u,video=obj))
        if purchased: return response('yes')
        else: return response('no')
    def purchase_video(self,request):
        u = self.current_user(request)
        o,t = request.POST['object'].split(';')
        now,objs,rel = self.get_object_bydate(o,t)
        obj = globals()[objs].objects.all().filter(date=now)[0]
        pp = PlayablePurchased(owner=u,video=obj)
        pp.save()
        return response('Video purchased.')