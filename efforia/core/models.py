from django.db.models import ForeignKey,IntegerField,Model,DateTimeField,TextField,CharField,DecimalField
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
    
class Place(Model):
    user = ForeignKey(User,unique=True)
    street = CharField(default="",max_length=100)
    city = CharField(default="",max_length=100)
    country = CharField(default="",max_length=50)
    latitude = DecimalField(max_digits=8, decimal_places=2)
    longitude = DecimalField(max_digits=8, decimal_places=2)
    
class Event(Model):
    name = CharField(default="",max_length=50)
    start_time = DateTimeField(default=date.today())
    end_time = DateTimeField(default=date.today())
    location = CharField(default="",max_length=100)
    id_event = CharField(default="",max_length=15)
    rsvp_status = CharField(default="",max_length=30)
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])