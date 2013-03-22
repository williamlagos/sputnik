import json
from django.contrib.auth.models import User
from django.http import HttpResponse as response

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
        # TODO: Separar filtragem e busca para um segundo momento
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
        print data
        if 'username' not in data or 'password' not in data:
            return response(json.dumps({'error':'User or password missing'}),
                            mimetype = 'application/json')
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

#class TwitterPosts(Coronae,TwitterHandler):
#    def get(self):
#        name = self.current_user().username
#        text = unicode('%s !%s' % (self.request.arguments['content'][0],name))
#        limit = 135-len(name)
#        if len(self.request.arguments['content']) > limit: 
#            short = unicode('%s... !%s' % (self.request.arguments['content'][0][:limit],name))
#        else: short = text
#        twitter = self.current_user().profile.twitter_token
#        if not twitter: twitter = get_offline_access()['twitter_token']
#        access_token = self.format_token(twitter)
#        encoded = short.encode('utf-8')
#        self.twitter_request(
#            "/statuses/update",
#            post_args={"status": encoded},
#            access_token=access_token,
#            callback=self.async_callback(self.posted))
#        self.write('Postagem tuitada com sucesso.')
#    def posted(self,response): pass
#
#class FacebookPosts(Coronae,FacebookHandler):
#    def get(self):
#        facebook = self.current_user().profile.facebook_token
#        if facebook:
#            name = self.current_user().username
#            text = unicode('%s !%s' % (self.request.arguments['content'],name))
#            encoded_facebook = text.encode('utf-8')
#            self.facebook_request("/me/feed",post_args={"message": encoded_facebook},
#                              access_token=facebook,
#                              callback=self.async_callback(self.posted))
#            self.write('Postagem publicada com sucesso.')
#    def posted(self,response): pass
#    
#class FacebookEvents(Coronae,FacebookHandler):
#    def get(self):
#        name = self.request.arguments['name'][0]
#        times = self.request.arguments['start_time'][0],self.request.arguments['end_time'][0]
#        dates = []
#        for t in times: 
#            strp_time = time.strptime(t,'%d/%m/%Y')
#            dates.append(datetime.fromtimestamp(time.mktime(strp_time)))
#        facebook = self.current_user().profile.facebook_token
#        if facebook:
#            args = { 'name':name, 'start_time':dates[0], 'end_time':dates[1] }
#            self.facebook_request("/me/events",access_token=facebook,post_args=args,
#                                  callback=self.async_callback(self.posted))
#    def posted(self): pass
