from models import UserProfile
from forms import RegisterForm
from djtornado import BaseHandler

class RegisterHandler(BaseHandler):
    def get(self):
        form = RegisterForm() # An unbound form
        return self.render("../templates/registration/register.html",title="My title",form=form)
    def post(self):
        form = RegisterForm()
        if form.is_valid():
            newuser = form.registerUser()
            profile = UserProfile(user=newuser,age=form.data['age'])
            profile.save()
            return self.redirect('/login/') # Redirect after POST
        else:
            return self.render('../templates/registration/register.html',form=form)