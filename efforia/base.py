from django.contrib.auth.models import User
from django.db.models import Model
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.utils.functional import curry

import tornado.web
import tornado.escape

class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj))
        return JSONEncoder.default(self,obj)

dumps = curry(dumps, cls=DjangoJSONEncoder)

class BaseHandler(tornado.web.RequestHandler):
    def to_json(self,obj):
        if isinstance(obj, QuerySet):
            return dumps(obj, cls=DjangoJSONEncoder)
        if isinstance(obj, Model):
            #do the same as above by making it a queryset first
            set_obj = [obj]
            set_str = dumps(loads(serialize('json', set_obj)))
            #eliminate brackets in the beginning and the end 
            str_obj = set_str[1:len(set_str)-2]
        return str_obj
    def get_login_url(self):
        return u"/login"
    def get_current_user(self):
        user_json = self.get_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None
    def authenticate(self,username,password):
        exists = User.objects.filter(username=username)
        if exists:
            #if password == username[::-1]: 
            return self.to_json(exists)
        else: return None
        