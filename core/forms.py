from django.forms import ModelForm
from models import Post,UserProfile

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

class RegisterForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('points','user')
        
