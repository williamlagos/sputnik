#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from handlers import BaseHandler,append_path
from stream import StreamService
append_path()

from forms import SpreadForm
from models import Spreadable,Relation
from tornado.auth import FacebookGraphMixin

class SocialHandler(BaseHandler):
    def get(self):
        if not self.authenticated(): return
        service = StreamService()
        feed = service.videos_by_user("VEVO")
        return self.srender('social.html',feed=feed)
    def twitter_credentials(self):
        credentials = {}
        user = self.current_user()
        credentials['user_id'] = user.username
        credentials['screen_name'] = user.email[1:]
        credentials['secret'] = user.profile.twitter_token.split(';')[0]
        credentials['key'] = user.profile.twitter_token.split(';')[1]
        return credentials
    def srender(self,place,**kwargs):
        user = self.current_user()
        kwargs['user'] = user
        today = datetime.today()
        birth = user.profile.birthday
        years = today.year-birth.year
        if today.month >= birth.month: pass
        elif today.month is birth.month and today.day >= birth.day: pass 
        else: years -= 1
        kwargs['birthday'] = years
        self.render(self.templates()+place,**kwargs)

class FavoritesHandler(SocialHandler):
    def get(self):
        self.srender('favorites.html',
                     known=self.current_relations(),
                     favorites=self.favorites())
    def favorites(self):
        service = StreamService()
        return service.videos_by_user("AdeleVEVO")
    def current_relations(self):
        if not self.authenticated(): return
        user = self.current_user()
        relations = Relation.objects.filter(user=user)    
        rels = []
        for r in relations: rels.append(r.known)
        return rels

class SpreadHandler(SocialHandler,FacebookGraphMixin):
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
        self.facebook_request("/me/feed",post_args={"message": text},
                              access_token=self.current_user().profile.facebook_token,
                              callback=self.async_callback(self._on_post))
        post = Spreadable(user=self.current_user(),content=text)
        return post
    def _on_post(self):
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
        model = Relation()
        user = self.current_user()
        model.user = user
        known = self.parse_request(self.request.uri)
        model.known = self.get_another_user(known)
        model.save()
        return self.redirect("/")
