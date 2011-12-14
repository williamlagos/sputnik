from django.db import models
from django.contrib.auth.models import User

class Spread(models.Model):
    user = models.ForeignKey(User, unique=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    points = models.IntegerField(default=0)
    age = models.IntegerField()
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

