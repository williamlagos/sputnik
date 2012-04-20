from django.db.models import ForeignKey,CharField,TextField,DateTimeField,Model
from django.contrib.auth.models import User

class Causable(Model):
    user = ForeignKey(User)
    title = CharField(max_length=100)
    content = TextField()
    video = TextField()
    date = DateTimeField(auto_now_add=True)