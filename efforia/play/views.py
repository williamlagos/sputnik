#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from handlers import append_path
from stream import StreamService
append_path()

from models import *
from create.models import Causable
from spread.views import SocialHandler
from StringIO import StringIO

class CollectionHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        self.render(self.templates()+'collection.html')

class FeedHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        service = StreamService()
        feed = service.top_rated()
        return self.render(self.templates()+'play.html',feed=feed)
    def post(self):
        token = self.parse_request(self.request.body)
        service = StreamService()
        feed = service.top_rated()
        return self.srender('play.html',feed=feed,token=token)

    
class UploadHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        return self.srender('expose.html')
    def post(self):
        title = "Efforia"
        description = "Vemos um mundo plural."
        service = StreamService()
        response = service.video_entry(title,description)
        video_io = StringIO()
        video = self.request.files["file"][0]
        video_io.write(video["body"])
        service.insert_video(response,video_io,video["content_type"])
        playable = Playable(user=self.current_user(),title=title,description=description,token='teste')
        playable.save()
        self.redirect('/')
    def get_form(self,title="Um teste",description="Este foi um teste."):
        service = StreamService()
        return service.video_entry(title,description)

class ScheduleHandler(SocialHandler):
    def get(self):
        if "action" in self.request.arguments:
            play = Playable.objects.all().filter(user=self.current_user)
            cause = Causable.objects.all().filter(user=self.current_user)
            self.srender('action.html',play=play,cause=cause)
        else: 
            play = PlaySchedule.objects.all().filter(user=self.current_user)
            cause = CauseSchedule.objects.all().filter(user=self.current_user)
            message = ""
            if not len(play) and not len(cause):
                message = "Você não possui nenhuma programação no momento. Gostaria de criar uma?"
            else:
                scheds = len(PlaySchedule.objects.filter(user=self.current_user()).values('name').distinct())
                message = '%i Programações de vídeos disponíveis' % scheds
            self.srender('schedule.html',message=message)
    def post(self):
        playables = []
        objects = self.get_argument('objects')
        title = self.get_argument('title')
        objs = urllib.unquote_plus(str(objects)).split(',')
        for o in objs: playables.append(Playable.objects.all().filter(token=o)[0])
        for p in playables: 
            playsched = PlaySchedule(user=self.current_user(),play=p,name=title)
            playsched.save()
        scheds = len(PlaySchedule.objects.all().filter(user=self.current_user(),name=title))
        self.srender('schedule.html',message='%i Programações de vídeos disponíveis' % scheds)
