from django.forms import Form,CharField,EmailField,PasswordInput,Textarea
from django.contrib.auth.models import User

class FriendSearch(Form):
    name = CharField(label="")

class SpreadForm(Form):
    content = CharField(label="",widget=Textarea)

class AuthorizeForm(Form):
    code = CharField(label="Code")#,help_text="The authorization code that Google returned to your redirect_uri in step 3.")
    client_id = CharField(label="Client ID",initial="416575314846.apps.googleusercontent.com")#,help_text="The OAuth 2.0 client ID for your application.")
    client_secret = CharField(label="Client Secret",initial="4O7-8yKLovNcwWfN5fzA2ptD")#,help_text="The client secret associated with your client ID. This value is displayed in the Google APIs console.")
    redirect_uri = CharField(label="Redirect URI",initial="http://efforia.herokuapp.com/oauth2callback")#,help_text="A registered redirect_uri for your client ID.")
    grant_type = CharField(label="Grant Type",initial="authorization_code")#,help_text="Set this value to authorization_code.")

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
