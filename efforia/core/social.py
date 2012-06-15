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

class GoogleOAuth2Mixin():
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

class GoogleHandler(tornado.web.RequestHandler,
                    GoogleOAuth2Mixin):
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

class TwitterHandler(tornado.web.RequestHandler,tornado.auth.TwitterMixin,tornado.auth.OAuthMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
    def authenticate_redirect(self):
        """Just like authorize_redirect(), but auto-redirects if authorized.

        This is generally the right interface to use if you are using
        Twitter for single-sign on.
        """
        http = Client()
        response = http.fetch(self._oauth_request_token_url())
        address = self.authenticate_twitter('http://api.twitter.com/oauth/authenticate',response)
        print address
        self.redirect(address)
    def authenticate_twitter(self, authorize_url, response):
        request_token = urlparse.parse_qs(response.body)
        data = (base64.b64encode(request_token["oauth_token"][0]) + "|" +
                base64.b64encode(request_token["oauth_token_secret"][0]))
        self.set_cookie("_oauth_request_token", data)
        args = { 
                'oauth_token': request_token["oauth_token"],
                'oauth_consumer_key': twitter_api['client_key'],
                'oauth_signature_method': "HMAC-SHA1",
                'oauth_timestamp': str(int(time.time())),
                'oauth_nonce': binascii.b2a_hex(uuid.uuid4().bytes),
                'oauth_version': '1.0'
        }
        signature = self._oauth_signature(twitter_api['client_key'], 'GET', 'http://api.twitter.com/oauth/access_token', args, request_token['oauth_token'])
        args["oauth_signature"] = signature
        return authorize_url + "?" + urllib.urlencode(args)
    def _oauth_signature(self,consumer_token, method, url, parameters={}, token=None):
        parts = urlparse.urlparse(url)
        scheme, netloc, path = parts[:3]
        normalized_url = scheme.lower() + "://" + netloc.lower() + path
    
        base_elems = []
        base_elems.append(method.upper())
        base_elems.append(normalized_url)
        base_elems.append("&".join("%s=%s" % (k, self._oauth_escape(str(v)))
                                   for k, v in sorted(parameters.items())))
        base_string =  "&".join(self._oauth_escape(e) for e in base_elems)
    
        key_elems = [tornado.escape.utf8(consumer_token["secret"])]
        key_elems.append(tornado.escape.utf8(token["secret"] if token else ""))
        key = "&".join(key_elems)
    
        hash = hmac.new(key, tornado.escape.utf8(base_string), hashlib.sha1)
        return binascii.b2a_base64(hash.digest())[:-1]
    def _oauth_escape(self,val):
        if isinstance(val, unicode):
            val = val.encode("utf-8")
        return urllib.quote(val, safe="~")
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500,"Twitter auth failed")
        access_token = user["access_token"]
        user_id = user["id_str"]
        data = urllib.urlencode({'twitter_token': access_token,'twitter_id': user_id})
        self.redirect("register?%s" % data)
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
