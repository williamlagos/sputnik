from models import UserProfile
from forms import RegisterForm,UserForm
from djtornado import BaseHandler
import urlparse
import tornado.web
import tornado.auth
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

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

class LoginHandler(BaseHandler):
    def get(self):
        form = AuthenticationForm()
        return self.render("../templates/registration/login.html",form=form)
    def post(self):
        request = self.get_django_request()
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            return self.redirect("/")
        else:
            form = AuthenticationForm(request)
        request.session.set_test_cookie()
        return self.render("../templates/registration/login.html",form=form)

class RegisterHandler(BaseHandler):
    def get(self):
        form = RegisterForm() # An unbound form
        return self.render("../templates/registration/register.html",form=form)
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