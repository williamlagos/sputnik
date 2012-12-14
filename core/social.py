import urllib,ast,base64,hmac,hashlib,binascii,urlparse,time,uuid
import tornado.web
import tornado.auth
import simplejson as json
from tornado.httpclient import HTTPClient as Client,HTTPRequest as Request,HTTPError
from tornado.escape import json_decode

def get_offline_access():
    apis = json.load(open('social.json','r'))
    facebook_api = apis['facebook']
    twitter_api = apis['twitter']
    google_api = apis['google']
    access = {
        'google_token': google_api['client_token'],
        'twitter_token': '%s;%s' % (twitter_api['client_token'],twitter_api['client_token_secret']),
        'facebook_token': facebook_api['client_token']
    }
    return access

class GoogleOAuth2Mixin(tornado.auth.OAuth2Mixin):
    def authorize_redirect(self,client_id,redirect_uri,scope):
        apis = json.load(open('social.json','r'))
        google_api = apis['google']
        oauth2_url = google_api['oauth2_url']
        redirect_uri = redirect_uri; client_id = client_id; scope = scope
        oauth2_url = "%sclient_id=%s&redirect_uri=%s&scope=%s&response_type=code" % (oauth2_url,client_id,redirect_uri,scope)
        self.redirect(oauth2_url)
    def authorize_first_redirect(self,client_id,redirect_uri,scope):
        apis = json.load(open('social.json','r'))
        google_api = apis['google']
        oauth2_url = google_api['oauth2_url']
        redirect_uri = redirect_uri; client_id = client_id; scope = scope
        oauth2_url = "%sclient_id=%s&redirect_uri=%s&scope=%s&response_type=code&access_type=offline&approval_prompt=force" % (oauth2_url,client_id,redirect_uri,scope)
        self.redirect(oauth2_url)
    def get_token_refreshed(self,client_id,client_secret,refresh_token):
        apis = json.load(open('social.json','r'))
        google_api = apis['google']
        if not refresh_token: refresh_token = get_offline_access()['google_token']
        data = {
            'client_id':     client_id,
            'client_secret': client_secret,
            'refresh_token':  refresh_token,
            'grant_type':    'refresh_token'
        }
        response = self.google_request(google_api['oauth2_token_url'],data)
        return json_decode(response.body)['access_token']
    def get_authenticated_user(self,redirect_uri,client_id,client_secret,code):
        apis = json.load(open('social.json','r'))
        google_api = apis['google']
        data = {
            'code':          code,
            'client_id':     client_id,
            'client_secret': client_secret,
            'redirect_uri':  redirect_uri,
            'grant_type':    'authorization_code'
        }
        return self.google_request(google_api['oauth2_token_url'],data)
    def google_request(self,url,body='',headers={}):
        client = Client()
        if not body: response = client.fetch(url)
        else:
            if not headers: response = client.fetch(Request(url,'POST',body=urllib.urlencode(body)))
            else: response = client.fetch(Request(url,'POST',headers,body))
        return response 

class GoogleHandler(tornado.web.RequestHandler,GoogleOAuth2Mixin):
    @tornado.web.asynchronous
    def get(self):
        apis = json.load(open('social.json','r'))
        google_api = apis['google']
        if self.get_argument("code",False):
            response = self.get_authenticated_user(
                redirect_uri =  google_api['redirect_uri'],
                client_id =     google_api['client_id'],
                client_secret = google_api['client_secret'],
                code =          self.get_argument("code"))
            tokens = json_decode(response.body)
            profile = self.google_credentials(tokens['access_token'],True)['id']
            if 'refresh_token' not in tokens: token = 'empty'
            else: token = tokens['refresh_token']
            self.redirect("register?google_id=%s&google_token=%s" % (profile,token))
        else: self.authorize_redirect(google_api['client_id'],
                                      google_api['redirect_uri'],
                                      google_api['authorized_apis'])
    def google_credentials(self,google,access_token=False):
        apis = json.load(open('social.json','r'))
        google_api = apis['google']
        if not access_token: token = self.refresh_token(google)
        else: token = google
        google_token = urllib.unquote_plus(token)
        url = '%s?access_token=%s' % (google_api['credentials'],google_token)
        response = self.google_request(url)
        return json_decode(response.body)
    def approval_prompt(self):
        apis = json.load(open('social.json','r'))
        google_api = apis['google']
        self.authorize_first_redirect(google_api['client_id'],
                                      google_api['redirect_uri'],
                                      google_api['authorized_apis'])
    def refresh_token(self,token):
        apis = json.load(open('social.json','r'))
        google_api = apis['google']
        return self.get_token_refreshed(google_api['client_id'],
                                        google_api['client_secret'],
                                        token)

class TwitterHandler(tornado.web.RequestHandler,tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self.authenticated))
            return
        self.authenticate_redirect()
    def authenticated(self, user):
        if not user:
            raise tornado.web.HTTPError(500,"Twitter auth failed")
        access_token = user["access_token"]
        user_id = user["id_str"]
        data = urllib.urlencode({'twitter_token': access_token,'twitter_id': user_id})
        self.redirect("register?%s" % data)
    def format_token(self,token):
        key,secret = token.split(';')
        tokens = { 'key': key, 'secret': secret }
        return tokens
    def twitter_credentials(self,token):
        apis = json.load(open('social.json','r'))
        twitter_api = apis['twitter']
        t = ast.literal_eval(urllib.unquote_plus(str(token)))
        twitter_token = "%s;%s" % (t['secret'],t['key'])
        self.twitter_request(twitter_api['credentials'],access_token=t,callback=self.async_callback(self._on_twitter_response))
        return twitter_token

class FacebookHandler(tornado.web.RequestHandler,tornado.auth.FacebookGraphMixin):
    @tornado.web.asynchronous
    def get(self):
        apis = json.load(open('social.json','r'))
        facebook_api = apis['facebook']
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
        fields = ['id','name','first_name','last_name','link','birthday','picture']
        self.facebook_request("/me",access_token=token,callback=self.async_callback(self._on_facebook_response),fields=fields)
        return facebook_token
