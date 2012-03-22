from django.db.models import ForeignKey,IntegerField,Model,CharField
from django.contrib.auth.models import User

class UserProfile(Model):
    user = ForeignKey(User,unique=True)
    points = IntegerField(default=0)
    age = IntegerField(default=0)
    google_token = CharField(default="null",max_length=60)
    twitter_token = CharField(default="null",max_length=60)
    facebook_token = CharField(default="null",max_length=120)
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])