from django.forms import Form,CharField,EmailField,PasswordInput
from django.contrib.auth.models import User

class RegisterForm(Form):
    username = CharField(label="Usuario")
    password = CharField(widget=PasswordInput,label="Senha")
    email = EmailField()
    first_name = CharField(label="Nome")
    last_name = CharField(label="Sobrenome")
    age = CharField(label="Idade")
