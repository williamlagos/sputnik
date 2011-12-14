from django.forms import ModelForm,Form,CharField,EmailField
from django.contrib.auth.models import User
from models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('user',)
    def save(self, user, commit = True):
        post = super(PostForm, self).save(commit = False)
        post.user = user
        if commit:
            post.save()
        return post

class RegisterForm(Form):
    username = CharField()
    password = CharField()
    email = EmailField()
    first_name = CharField()
    last_name = CharField()
    age = CharField()
    def registerUser(self):
        user = User.objects.create_user(self.data['username'],
                                        self.data['email'],
                                        self.data['password'])
        user.last_name = self.data['last_name']
        user.first_name = self.data['first_name']
        user.save()
        return user