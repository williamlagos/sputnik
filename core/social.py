import json,urllib,oauth2 as oauth
from datetime import datetime
from time import mktime,strptime
from django.contrib.auth.models import User
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect

from models import *
from spread.models import *
from promote.models import *
from main import Efforia

objs = json.load(open('settings.json','r'))

class Search(Efforia):
    def __init__(self): pass
    def explore(self,request):
        try: query = request.GET['explore']
        except KeyError,e: query = ''
        #filters = request.GET['filters']
        #filtr = filters.split(',')[:-1]
        mixed = []
        for o in objs['objects']:
            #filter_index = normalize('NFKD', f.decode('utf-8')).encode('ASCII','ignore')
            queryset = globals()[o].objects.all()
            filter(lambda obj: query.lower() in obj.name.lower(),queryset)  
            if 'Movement' in o: self.group_movement(queryset,mixed)
            else: mixed.extend(queryset)
        #shuffle(mixed)
        return self.view_mosaic(request,mixed)
        
class Follows(Efforia):
    def __init__(self): pass
    def view_following(self,request):
        u = self.current_user(request); rels = []
        for f in Followed.objects.filter(follower=u.id):
            rels.append(Profile.objects.filter(id=f.followed)[0])
        return self.view_mosaic(request,rels)
    def become_follower(self,request):
        u = self.current_user(request).id
        followed = Profile.objects.filter(id=request.GET['profile_id'])[0].user_id
        follow = Followed(followed=followed,follower=u)
        follow.save()
        return response('Profile followed successfully')
    def leave_follower(self,request):
        u = self.current_user(request).id
        followed = request.GET['profile_id']
        query = Followed.objects.filter(followed=followed,follower=u)
        if len(query): query[0].delete()
        return response('Profile unfollowed successfully')


class ID(Efforia):
    def __init__(self): pass
    def view_id(self,request):
        u = self.current_user(request)
        if 'first_turn' in request.GET:
            if u.profile.first_turn: return response('yes')
            else: return response('no')
        elif 'object' in request.GET:
            o,t = request.GET['object'][0].split(';')
            now,objs,rels = self.get_object_bydate(o,t)
            obj = globals()[objs].objects.all().filter(date=now)[0]
            if hasattr(obj,'user'): return response(str(obj.user.id))
            else: return response(str(self.current_user().id))
        else: return response(str(self.current_user().id))
    def finish_tutorial(self,request):
        u = self.current_user(request)
        p = Profile.objects.all().filter(user=u)[0]
        p.first_time = False
        p.save()
        return response('Tutorial finalizado.')        

class Deletes(Efforia):
    def delete_element(self,request):
        oid = request.GET['id']
        obj = self.object_token(request.GET['token'])[0]
        query = globals()[obj].objects.filter(id=oid)
        if len(query): query[0].delete()
        return response('Object deleted successfully')
    
class Authentication(Efforia):              
    def authenticate(self,request):
        data = request.REQUEST
        if 'profile' in data:
            profile = self.json_decode(data['profile'])
            # Atualizacao do perfil com tokens sociais
            if 'user' in request.session:
                u = self.current_user(request)
                p = Profile.objects.filter(user=u)[0]
                types = data['social']
                if 'google' in types: p.google_token = profile['google_token'] 
                elif 'twitter' in types: p.twitter_token = '%s;%s' % (profile['key'],profile['secret'])
                elif 'facebook' in types: p.facebook_token = profile['facebook_token']
                p.save()       
                return redirect('/')
            # Registro do perfil com token social
            else:
                return response(json.dumps(profile),mimetype='application/json')
        elif 'username' not in data or 'password' not in data:
            return response(json.dumps({'error':'User or password missing'}),
                            mimetype = 'application/json')
        else:
            username = data['username']
            password = data['password']
            exists = User.objects.filter(username=username)
            if exists:
                if exists[0].check_password(password):
                    obj = json.dumps({'username':username,'userid':exists[0].id})
                    request.session['user'] = username
                    return response(json.dumps({'success':'Login successful'}),
                                    mimetype = 'application/json')
                else:
                    obj = json.dumps({'error':'User or password wrong'})
                    return response(obj,mimetype='application/json')
    def leave(self,request):
        del request.session['user']
        return response(json.dumps({'success':'Logout successful'}),mimetype='application/json')

class Twitter(Efforia):
    def update_status(self,request):
        u = self.current_user(request)
        if len(request.GET['content']) > 137: 
            short = unicode('%s...' % (request.GET['content'][:137]))
        else: short = unicode('%s' % (request.GET['content']))
        tokens = u.profile.twitter_token
        if not tokens: tokens = self.own_access()['twitter_token']
        data = {'status':short.encode('utf-8')}
        self.oauth_post_request('/statuses/update.json',tokens,data,'twitter')
        return response('Published posting successfully on Twitter')

class Google(Efforia):
    def update_status(self,request):
        return response('Hello World!')

class Facebook(Efforia):
    def update_status(self,request):
        u = self.current_user(request)
        token = u.profile.facebook_token
        text = unicode('%s' % request.GET['content'])
        data = {'message':text.encode('utf-8')}
        self.oauth_post_request("/me/feed",token,data,'facebook')
        return response('Published posting successfully on Facebook')
    def send_event(self,request):
        u = self.current_user(request)
        token = u.profile.facebook_token
        name = request.GET['name']; dates = []
        d = request.GET['start_time'],request.GET['end_time']
        for t in d: dates.append(date.fromtimestamp(mktime(strptime(t,'%d/%m/%Y'))))
        data = {'name':name,'start_time':dates[0],'end_time':dates[1]}
        self.oauth_post_request("/me/events",token,data,'facebook')
        return response('Published event successfully on Facebook')
