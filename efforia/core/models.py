from django.db.models import ForeignKey,IntegerField,Model,DateTimeField,TextField,CharField
from django.contrib.auth.models import User
from datetime import date

class UserProfile(Model):
    user = ForeignKey(User,unique=True)
    points = IntegerField(default=0)

    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])