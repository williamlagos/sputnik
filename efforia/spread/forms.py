from django.forms import Form,CharField,EmailField,PasswordInput
from django.contrib.auth.models import User

class FriendSearch(Form):
    name = CharField()

class SpreadForm(Form):
    content = CharField(label="Conteudo")

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
