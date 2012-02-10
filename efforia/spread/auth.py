from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from models import UserProfile
from forms import RegisterForm
from base import BaseHandler
import tornado.web
import tornado.auth

class LoginHandler(BaseHandler):    
    def get(self):
        form = AuthenticationForm()
	form.fields["username"].label = "Nome"
	form.fields["password"].label = "Senha"
        self.render(self.templates()+"registration/login.html", next=self.get_argument("next","/"), form=form)
    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.authenticate(username,password) # DB lookup here
        if auth is not None:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", "/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
            self.redirect(u"/login" + error_msg)
    def set_current_user(self, user):
        if user:
            self.set_cookie("user",tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/login")

class GoogleHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        # Save the user with, e.g., set_secure_cookie()

class FacebookHandler(LoginHandler, tornado.auth.FacebookGraphMixin):
	@tornado.web.asynchronous
	def initialize(self):
		self.settings["facebook_api_key"] = "153246718126522"
		self.settings["facebook_secret"] = "15f57d59a69b96c3d3013b4c9aa301f2"
	def get(self):
		self.initialize()
		if self.get_argument("code", False):
			self.get_authenticated_user(
				redirect_uri='/auth/facebookgraph/',
				client_id=self.settings["facebook_api_key"],
				client_secret=self.settings["facebook_secret"],
				code=self.get_argument("code"),
				callback=self.async_callback(
				self._on_login))
			return
		self.authorize_redirect(redirect_uri='/auth/facebookgraph/',
                              		client_id=self.settings["facebook_api_key"],
		                        extra_params={"scope": "read_stream,offline_access"})
	def _on_login(self, user):
		logging.error(user)
		self.finish()

class RegisterHandler(BaseHandler):
    def get(self):
        form = RegisterForm() # An unbound form
        return self.render(self.templates()+"registration/register.html",form=form)
    def post(self):
        data = {
            'username':self.request.arguments['username'][0],
            'email':self.request.arguments['email'][0],
            'password':self.request.arguments['password'][0],
            'last_name':self.request.arguments['last_name'][0],
            'first_name':self.request.arguments['first_name'][0],
            'age':self.request.arguments['age'][0],
        }
        form = RegisterForm(data=data)
        newuser = form.registerUser()
        profile = UserProfile(user=newuser,age=form.data['age'])
        profile.save()
        return self.redirect('/login') # Redirect after POST
