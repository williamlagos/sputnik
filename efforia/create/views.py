#!/usr/bin/python
# -*- coding: utf-8 -*-
from tornado.auth import TwitterMixin
from StringIO import StringIO
from forms import CausesForm
from stream import StreamService
from handlers import append_path
append_path()

from spread.views import SocialHandler

class CausesHandler(SocialHandler,TwitterMixin):
    def get(self):
        form = CausesForm()
        self.srender("create.html",form=form)
    def post(self):
        title = "#%s" % self.get_argument("title").replace(" ","")
        text = u"%s " % self.get_argument("content")
        service = StreamService()
        response = service.video_entry("Teste","Isto foi um teste.")
        video_io = StringIO()
        video = self.request.files["file"][0]
        video_io.write(video["body"])
        resp = service.insert_video(response,video_io,video["content_type"])
        print resp
        cred = self.twitter_credentials()
        self.twitter_request(path="/statuses/update",access_token=cred,
                             callback=self.async_callback(self.on_post),post_args={"status": text+title})
    def on_post(self,response):
        self.finish()