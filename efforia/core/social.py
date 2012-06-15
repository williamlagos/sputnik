import urllib,ast,base64,hmac,hashlib,binascii,urlparse,time,uuid
import tornado.web
import tornado.auth
import simplejson as json
import tornado.httpclient
from tornado.httpclient import HTTPClient as Client,HTTPRequest as Request,HTTPError
from tornado.escape import json_decode

apis = json.load(open('social.json','r'))
facebook_api = apis['facebook']
twitter_api = apis['twitter']
google_api = apis['google']

class GoogleOAuth2Mixin(tornado.auth.OAuth2Mixin):
    def authorize_redirect(self,client_id,redirect_uri,scope):
        oauth2_url = google_api['oauth2_url']
        redirect_uri = redirect_uri; client_id = client_id; scope = scope
        oauth2_url = "%sclient_id=%s&redirect_uri=%s&scope=%s&response_type=code" % (oauth2_url,client_id,redirect_uri,scope)
        self.redirect(oauth2_url)
    def authorize_first_redirect(self,client_id,redirect_uri,scope):
        oauth2_url = google_api['oauth2_url']
        redirect_uri = redirect_uri; client_id = client_id; scope = scope
        oauth2_url = "%sclient_id=%s&redirect_uri=%s&scope=%s&response_type=code&access_type=offline&approval_prompt=force" % (oauth2_url,client_id,redirect_uri,scope)
        self.redirect(oauth2_url)
    def get_token_refreshed(self,client_id,client_secret,refresh_token):
        data = {
            'client_id':     client_id,
            'client_secret': client_secret,
            'refresh_token':  refresh_token,
            'grant_type':    'refresh_token'
        }
        print data
        print google_api['oauth2_token_url']
        response = self.google_request(google_api['oauth2_token_url'],data)
        return json_decode(response.body)['access_token']
    def get_authenticated_user(self,redirect_uri,client_id,client_secret,code):
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

class TwitterOAuthMixin(tornado.auth.OAuthMixin):
    def authenticate_redirect(self):
        http = Client()
        request_token_url = 'http://api.twitter.com/oauth/request_token?'
        authenticate_url = 'http://api.twitter.com/oauth/authenticate?'
        args = urllib.urlencode(self.get_parameters(request_token_url))
        request_token = self.set_request_token(http.fetch(request_token_url+args))
        oauth = self.get_oauth_parameters('http://api.twitter.com/oauth/access_token',request_token['oauth_token'][0],request_token['oauth_token_secret'][0])
        authenticate = authenticate_url+urllib.urlencode(oauth)
        print "AUTHENTICATE URLS"
        print authenticate
        print authenticate_url+'oauth_token='+request_token['oauth_token'][0]
        self.redirect(authenticate)
    def set_request_token(self,token):
        print "REQUEST TOKEN BODY"
        print token.body
        request_token = urlparse.parse_qs(token.body)
        data = (base64.b64encode(request_token["oauth_token"][0]) + "|" +
                base64.b64encode(request_token["oauth_token_secret"][0]))
        self.set_cookie("_oauth_request_token", data)
        return request_token
    def get_parameters(self,url):
        args = {
                'oauth_consumer_key': twitter_api['client_key'],
                'oauth_signature_method': "HMAC-SHA1",
                'oauth_timestamp': str(int(time.time())),
                'oauth_nonce': binascii.b2a_hex(uuid.uuid4().bytes),
                'oauth_version': '1.0'
        }
        args["oauth_signature"] = self.signature(twitter_api['client_secret'],"GET",url, args)
        return args
    def get_oauth_parameters(self,url,oauth_token,oauth_token_secret):
        args = { 
                'oauth_token': oauth_token,
                'oauth_consumer_key': twitter_api['client_key'],
                'oauth_signature_method': "HMAC-SHA1",
                'oauth_timestamp': str(int(time.time())),
                'oauth_nonce': binascii.b2a_hex(uuid.uuid4().bytes),
                'oauth_version': '1.0'
        }
        args["oauth_signature"] = self.signature(twitter_api['client_secret'],'GET',url,args,oauth_token)
        return args
    def signature(self,consumer_token, method, url, parameters={}, token=None):
        parts = urlparse.urlparse(url)
        scheme, netloc, path = parts[:3]
        normalized_url = scheme.lower() + "://" + netloc.lower() + path
        base_elems = []
        base_elems.append(method.upper())
        base_elems.append(normalized_url)
        base_elems.append("&".join("%s=%s" % (k, self.escape(str(v)))
                                   for k, v in sorted(parameters.items())))
        base_string =  "&".join(self.escape(e) for e in base_elems)
        key_elems = [tornado.escape.utf8(consumer_token)]
        key_elems.append(tornado.escape.utf8(token if token else ""))
        key = "&".join(key_elems)
    
        hash = hmac.new(key, tornado.escape.utf8(base_string), hashlib.sha1)
        return binascii.b2a_base64(hash.digest())[:-1]
    def escape(self,val):
        if isinstance(val, unicode):
            val = val.encode("utf-8")
        return urllib.quote(val, safe="~")
    def twitter_request(self,path,token=None,token_secret=None,post_args=None,**args):
        url = "http://api.twitter.com/1" + path + ".json"
        if token and token_secret:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            oauth = self.get_oauth_parameters(token,token_secret)
            args.update(oauth)
        if args: url += "?" + urllib.urlencode(args)
        print args
        http = Client()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args))
        else:
            http.fetch(url)
        

class GoogleHandler(tornado.web.RequestHandler,GoogleOAuth2Mixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("code",False):
            response = self.get_authenticated_user(
                redirect_uri =  google_api['redirect_uri'],
                client_id =     google_api['client_id'],
                client_secret = google_api['client_secret'],
                code =          self.get_argument("code"))
            tokens = json_decode(response.body)
            print tokens
            profile = self.google_credentials(tokens['access_token'],True)['id']
            if 'refresh_token' not in tokens: token = 'empty'
            else: token = tokens['refresh_token']
            self.redirect("register?google_id=%s&google_token=%s" % (profile,token))
        else: self.authorize_redirect(google_api['client_id'],
                                      google_api['redirect_uri'],
                                      google_api['authorized_apis'])
    def google_credentials(self,google,access_token=False):
        if not access_token: token = self.refresh_token(google)
        else: token = google
        google_token = urllib.unquote_plus(token)
        url = '%s?access_token=%s' % (google_api['credentials'],google_token)
        response = self.google_request(url)
        return json_decode(response.body)
    def approval_prompt(self):
        self.authorize_first_redirect(google_api['client_id'],
                                      google_api['redirect_uri'],
                                      google_api['authorized_apis'])
    def refresh_token(self,token):
        return self.get_token_refreshed(google_api['client_id'],
                                        google_api['client_secret'],
                                        token)

class TwitterHandler(tornado.web.RequestHandler,TwitterOAuthMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            print self.request.arguments
            self.redirect('/')
            #self.get_authenticated_user(self.async_callback(self.authenticated))
            #return
        self.authenticate_redirect()
    def authenticated(self,user):
        access_token = user["access_token"]
        user_id = user["id_str"]
        data = urllib.urlencode({'twitter_token': access_token,'twitter_id': user_id})
        self.redirect("register?%s" % data)
    def twitter_credentials(self,token):
        t,s = token.split(';')
        return self.twitter_request(twitter_api['credentials'],token=t,token_secret=s)

class FacebookHandler(tornado.web.RequestHandler,tornado.auth.FacebookGraphMixin):
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
