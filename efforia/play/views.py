#!/usr/bin/python
# -*- coding: utf-8 -*-
from handlers import append_path
from stream import StreamService
append_path()
from models import *
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
        play = PlaySchedule.objects.all().filter(user=self.current_user)
        cause = CauseSchedule.objects.all().filter(user=self.current_user)
        message = ""
        if not len(play) and not len(cause):
            message = "Você não possui nenhuma programação no momento. Gostaria de criar uma?"
        self.srender('schedule.html',message=message)
    def post(self):
        pass
