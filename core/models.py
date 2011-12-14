from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    points = models.IntegerField(default=0)
    first_name = models.CharField()
    last_name = models.CharField()
    age = models.IntegerField()
    username = models.CharField()
    password = models.CharField()
    email = models.CharField()
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

