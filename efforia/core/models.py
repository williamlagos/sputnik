from django.db.models import ForeignKey,IntegerField,Model,CharField,TextField
from django.contrib.auth.models import User

class UserProfile(Model):
    user = ForeignKey(User,unique=True)
    points = IntegerField(default=0)
    age = IntegerField(default=0)
    google_token = TextField(default="",max_length=120)
    twitter_token = TextField(default="",max_length=120)
    facebook_token = TextField(default="",max_length=120)
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])