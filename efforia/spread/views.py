from handlers import BaseHandler,append_path
from stream import StreamService
append_path()

from forms import SpreadForm
from models import Spreadable,UserRelation
from tornado.auth import TwitterMixin

class SocialHandler(BaseHandler):
    def get(self):
        if not self.authenticated(): return
        service = StreamService()
        feed = service.videos_by_user("VEVO")
        return self.srender('home.html',feed=feed)
    def favorites(self):
        service = StreamService()
        return service.videos_by_user("AdeleVEVO")
    def current_relations(self):
        if not self.authenticated(): return
        user = self.current_user()
        relations = UserRelation.objects.filter(user=user)	
        rels = []
        for r in relations: rels.append(r.known)
        return rels
    def twitter_credentials(self):
        credentials = {}
        user = self.current_user()
        credentials['user_id'] = user.username
        credentials['screen_name'] = user.email[1:]
        credentials['key'] = user.profile.twitter_token.split(';')[0]
        credentials['secret'] = user.profile.twitter_token.split(';')[1]
        return credentials
    def srender(self,place,**kwargs):
        kwargs['user'] = self.current_user()
        kwargs['known'] = self.current_relations()
        kwargs['favorites'] = self.favorites()
        self.render(self.templates()+place,**kwargs)

class SpreadHandler(SocialHandler):
    def post(self):
        if not self.authenticated(): return
        spread = self.spread()
        spread.save()
        return self.redirect('spreads')
    def get(self):
        if not self.authenticated(): return
        form = SpreadForm()
        self.srender("spread.html",form=form)
    def spread(self):
        text = self.parse_request(self.request.body)
        post = Spreadable(user=self.current_user(),content=text)
        return post

class CausesHandler(SocialHandler,TwitterMixin):
    def get(self):
        form = SpreadForm()
        self.srender("causes.html",form=form)
    def post(self):
        text = self.get_argument("content")
        cred = self.twitter_credentials()
        self.twitter_request("/statuses/update",post_args={"status": text},
                             access_token=cred,callback=self.async_callback(self.on_post))
    def on_post(self):
        self.finish()

class PostHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        user = self.current_user()
        spreads = Spreadable.objects.all().filter(user=user)
        return self.srender('spreads.html',spreads=spreads)

class KnownHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        model = UserRelation()
        user = self.current_user()
        model.user = user
        known = self.parse_request(self.request.uri)
        model.known = self.get_another_user(known)
        model.save()
        return self.redirect("/")
