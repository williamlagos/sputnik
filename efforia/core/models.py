from django.db.models import ForeignKey,IntegerField,Model,DateTimeField,TextField,CharField
from django.contrib.auth.models import User
from datetime import date

class UserProfile(Model):
    user = ForeignKey(User,unique=True)
    points = IntegerField(default=0)
    credit = IntegerField(default=0)
    visual = CharField(default="",max_length=30)
    birthday = DateTimeField(default=date.today())
    google_token = TextField(default="",max_length=120)
    twitter_token = TextField(default="",max_length=120)
    facebook_token = TextField(default="",max_length=120)
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])