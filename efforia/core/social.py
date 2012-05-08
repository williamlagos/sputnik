import urllib,urllib2
import tornado.web
import simplejson as json

class GoogleOAuth2Mixin():
    def authorize_redirect(self,client_id,redirect_uri,scope):
        oauth2_url = "https://accounts.google.com/o/oauth2/auth?"
        redirect_uri = redirect_uri; client_id = client_id; scope = scope
        oauth2_url = "%sclient_id=%s&redirect_uri=%s&scope=%s&response_type=code&access_type=offline" % (oauth2_url,client_id,redirect_uri,scope)
        self.redirect(oauth2_url)
    def get_authenticated_user(self,redirect_uri,client_id,client_secret,code):
        data = urllib.urlencode({
              'code':      code,
            'client_id':      client_id,
            'client_secret': client_secret,
            'redirect_uri':  redirect_uri,
            'grant_type':    'authorization_code'
        })
        return self.google_request('https://accounts.google.com/o/oauth2/token',data)
    def google_request(self,url,data):
        request = urllib2.Request(url=url,data=data)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return response

class TwitterHandler(tornado.web.RequestHandler,
                     tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")
        access_token = user["access_token"]
        data = urllib.urlencode({ 'twitter_token': access_token })
        self.redirect("register?%s" % data)
        self.finish()
        
class GoogleHandler(tornado.web.RequestHandler,
            GoogleOAuth2Mixin):
    def get(self):
        if self.get_argument("code",False):
            token = self.get_authenticated_user(
                redirect_uri="http://efforia.herokuapp.com/google",
                client_id="416575314846.apps.googleusercontent.com",
                client_secret="4O7-8yKLovNcwWfN5fzA2ptD",
                code=self.get_argument("code"))
            self.redirect("register?google_token=%s" % json.loads(token)['access_token'])
        self.authorize_redirect("416575314846.apps.googleusercontent.com",
                                "http://efforia.herokuapp.com/google",
                                "https://gdata.youtube.com+https://www.googleapis.com/auth/userinfo.profile")

class FacebookHandler(tornado.web.RequestHandler,
              tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri='http://efforia.herokuapp.com/facebook',
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_login))
            return
        self.authorize_redirect(redirect_uri='http://efforia.herokuapp.com/facebook',
                                      client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": "publish_stream,read_stream,user_birthday,user_events,create_event"})
    def _on_login(self, user):
        self.redirect("register?facebook_token=%s" % user['access_token'])