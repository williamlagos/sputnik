import urllib,urllib2,ast
import tornado.web
import tornado.auth
import simplejson as json
from tornado.httpclient import HTTPClient as Client,HTTPRequest as Request,HTTPError

apis = json.load(open('social.json','r'))
facebook_api = apis['facebook']
twitter_api = apis['twitter']
google_api = apis['google']

class GoogleOAuth2Mixin():
    def authorize_redirect(self,client_id,redirect_uri,scope):
        oauth2_url = google_api['oauth2_url']
        redirect_uri = redirect_uri; client_id = client_id; scope = scope
        oauth2_url = "%sclient_id=%s&redirect_uri=%s&scope=%s&response_type=code&access_type=online&approval_prompt=auto" % (oauth2_url,client_id,redirect_uri,scope)
        self.redirect(oauth2_url)
    def get_authenticated_user(self,redirect_uri,client_id,client_secret,code):
        data = {
            'code':          code,
            'client_id':     client_id,
            'client_secret': client_secret,
            'redirect_uri':  redirect_uri,
            'grant_type':    google_api['grant_type']
        }
        return self.google_request(google_api['oauth2_token_url'],data)
    def google_request(self,url,body='',headers={},method='POST'):
        client = Client()
        if 'GET' in method: response = client.fetch(url)
        elif not headers: response = client.fetch(Request(url,method='POST',body=urllib.urlencode(body)))
        else: response = client.fetch(Request(url,method,headers,body))
        return response

class GoogleHandler(tornado.web.RequestHandler,
                    GoogleOAuth2Mixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code",False):
            token = self.get_authenticated_user(
                redirect_uri =  google_api['redirect_uri'],
                client_id =     google_api['client_id'],
                client_secret = google_api['client_secret'],
                code =          self.get_argument("code"))
            print token.body
            self.redirect("register?google_token=%s" % tornado.escape.json_decode(token.body)['access_token'])
        self.authorize_redirect(google_api['client_id'],
                                google_api['redirect_uri'],
                                google_api['authorized_apis'])
    def google_credentials(self,token):
        google_token = urllib.unquote_plus(token)
        url = '%s?access_token=%s' % (google_api['credentials'],google_token)
        request = urllib2.Request(url=url)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return google_token,response

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
    def twitter_credentials(self,token):
        t = ast.literal_eval(urllib.unquote_plus(str(token)))
        twitter_token = "%s;%s" % (t['secret'],t['key'])
        self.twitter_request(twitter_api['credentials'],access_token=t,callback=self.async_callback(self._on_response))
        return twitter_token

class FacebookHandler(tornado.web.RequestHandler,
              tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=facebook_api['redirect_uri'],
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"),
                callback=self.async_callback(self._on_login))
            return
        self.authorize_redirect(redirect_uri=facebook_api['redirect_uri'],
                                client_id=self.settings["facebook_api_key"],
                                extra_params={"scope": facebook_api['authorized_apis']})
    def _on_login(self, user):
        self.redirect("register?facebook_token=%s" % user['access_token'])
    def facebook_credentials(self,token):
        facebook_token = urllib.unquote_plus(token)
        fields = ['id','first_name','last_name','link','birthday','picture']
        self.facebook_request("/me",access_token=token,callback=self.async_callback(self._on_response),fields=fields)
        return facebook_token
