import urllib2,json,ast
from datetime import datetime
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
    def do_request(self,url,data=""):
        request = urllib2.Request(url=url,data=data)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return response
    def object_token(self,token):
        objs = json.load(open('settings.json','r'))
        objects,relations = objs['tokens'][token]
        return objects,relations
    def object_byid(self,token,ident):
        obj = self.object_token(token)[0]
        return globals()[obj].objects.filter(id=ident)[0]
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