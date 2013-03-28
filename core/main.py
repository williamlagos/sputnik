import urllib2,urllib,json,ast,time
import oauth2 as oauth
from datetime import datetime,timedelta,date
from django.contrib.auth.models import User
from django.shortcuts import render
from django.conf import settings

from models import Profile,user
from spread.models import Page
from feed import Mosaic

class Efforia(Mosaic):
    def __init__(self): pass
    def start(self,request):
        if 'user' in request.session:
            # Painel do usuario
            u = user(request.session['user'])
            return render(request,'index.jade',{
                                                'static_url':settings.STATIC_URL,
                                                'user':user(request.session['user']),
                                                'name':'%s %s' % (u.first_name,u.last_name)
                                                },content_type='text/html')
        # Pagina inicial
        p = list(Page.objects.filter(user=user('efforia')))
        return render(request,'enter.jade',{'static_url':settings.STATIC_URL,'pages':p},content_type='text/html')
    def external(self,request):
        u = self.current_user(request)
        credits = int(request.POST['quantity'])
        profile = Profile.objects.all().filter(user=u)[0]
        profile.credit += credits
        profile.save()
        return self.redirect('/')
    def json_decode(self,string):
        j = json.loads(string,'utf-8')
        return ast.literal_eval(j)
    def url_request(self,url,data=None,headers={}):
        request = urllib2.Request(url=url,data=data,headers=headers)
        request_open = urllib2.urlopen(request)
        return request_open.geturl()
    def do_request(self,url,data=None,headers={}):
        request = urllib2.Request(url=url,data=data,headers=headers)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return response
    def oauth_post_request(self,url,tokens,data={},social='twitter'):
        api = json.load(open('settings.json','r'))['social']
        posturl ='%s%s'%(api[social]['url'],url)
        if 'facebook' in social:
            socialurl = '%s?%s'%(posturl,urllib.urlencode({'access_token':tokens}))
            if 'start_time' in data:
                data['end_time'] = data['end_time'].date()
                if data['end_time'] == date.today(): 
                    data['end_time'] = data['end_time']+timedelta(days=1)
                data['start_time'] = data['start_time'].date()
            return self.do_request(socialurl,urllib.urlencode(data))
        else:
            access_token,access_token_secret = tokens.split(';')
            token = oauth.Token(access_token,access_token_secret)
            consumer_key = api[social]['client_key']
            consumer_secret = api[social]['client_secret']
            consumer = oauth.Consumer(consumer_key,consumer_secret)
            client = oauth.Client(consumer,token)
            return client.request(posturl,'POST',urllib.urlencode(data))
    def refresh_google_token(self,token):
        api = json.load(open('settings.json','r'))['social']['google']
        if not token: token = self.own_access()['google_token']
        data = urllib.urlencode({
            'client_id':      api['client_id'],
            'client_secret':  api['client_secret'],
            'refresh_token':  token,
            'grant_type':    'refresh_token' })
        return json.loads(self.do_request(api['oauth2_token_url'],data))['access_token']
    def object_token(self,token):
        objs = json.load(open('settings.json','r'))
        objects,relations = objs['tokens'][token]
        return objects,relations
    def object_byid(self,token,ident):
        obj = self.object_token(token)[0]
        return globals()[obj].objects.filter(id=ident)[0]
    def convert_datetime(self,date_value):
        d = time.strptime(date_value,'%d/%m/%Y')
        return datetime.fromtimestamp(time.mktime(d))
    def authenticate(self,username,password):
        exists = User.objects.filter(username=username)
        if exists:
            if exists[0].check_password(password): 
                return exists
        else: return None
    def authenticated(self):
        name = self.get_current_user()
        if not name: 
            #self.redirect('login')
            self.render('templates/enter.html',STATIC_URL=settings.STATIC_URL)
            return False
        else:
            return True
    def accumulate_points(self,points,request=None):
        if request is None: u = self.current_user()
        else: u = self.current_user(request)
        current_profile = Profile.objects.all().filter(user=u)[0]
        current_profile.points += points
        current_profile.save()
    def own_access(self):
        objs = json.load(open('settings.json','r'))
        google_api = objs['social']['google']
        twitter_api = objs['social']['twitter']
        facebook_api = objs['social']['facebook']
        access = {
            'google_token': google_api['client_token'],
            'twitter_token': '%s;%s' % (twitter_api['client_token'],twitter_api['client_token_secret']),
            'facebook_token': facebook_api['client_token']
        }
        return access