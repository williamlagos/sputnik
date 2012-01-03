from django.forms import ModelForm,Form,CharField,EmailField,PasswordInput
from django.contrib.auth.models import User
from models import Spread,UserProfile

class FriendSearch(Form):
    name = CharField()
    def searchUser(self):
        found = User.objects.all().filter(first_name=self.data['name'])
        return found

class SpreadForm(ModelForm):
    class Meta:
        model = Spread
        exclude = ('user',)
    def save(self, user, commit = True):
        spread = super(SpreadForm, self).save(commit = False)
        spread.user = user
        if commit: spread.save()
        return spread

class RegisterForm(Form):
    username = CharField(label="Usuario")
    password = CharField(widget=PasswordInput,label="Senha")
    email = EmailField()
    first_name = CharField(label="Nome")
    last_name = CharField(label="Sobrenome")
    age = CharField(label="Idade")
    def registerUser(self):
        user = User.objects.create_user(self.data['username'],
                                        self.data['email'],
                                        self.data['password'])
        user.last_name = self.data['last_name']
        user.first_name = self.data['first_name']
        user.save()
        return user