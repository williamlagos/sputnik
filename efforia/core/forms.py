# -*- coding: utf-8 -*-

from django.forms import Form,CharField,EmailField,PasswordInput,ModelForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from models import Place

class RegisterForm(Form):
    username = CharField(label="Usuário")
    password = CharField(widget=PasswordInput,label="Senha")
    email = EmailField()
    first_name = CharField(label="Nome")
    last_name = CharField(label="Sobrenome")
    birthday = CharField(label="Aniversário")
    
class ProfileForm(Form):
    username = CharField(label="Usuario")
    email = EmailField()
    first_name = CharField(label="Nome")
    last_name = CharField(label="Sobrenome")
    
class PasswordForm(PasswordChangeForm):
    pass

class PlaceForm(ModelForm):
    email = EmailField()
    password = CharField(widget=PasswordInput,label="Senha")
    class Meta:
        model = Place
        exclude = ('latitude','longitude','user')
