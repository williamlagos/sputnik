from django.db.models import ForeignKey,CharField,TextField,DateTimeField,IntegerField,BooleanField,Model
from django.contrib.auth.models import User
from datetime import date
from efforia.models import Sellable

locale = ('Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez')

class Promoted(Model):
    name = CharField(default='@#',max_length=2)
    user = ForeignKey(User,related_name='+')
    prom = IntegerField(default=1)
    content = TextField()
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]    

class Project(Model):
    name = CharField(default='',max_length=50)
    user = ForeignKey(User)
    start_time = DateTimeField(default=date.today())
    end_time = DateTimeField(default=date.today())
    content = TextField(default='')
    credit = IntegerField(default=0)
    ytoken = CharField(default='',max_length=15)
    visual = CharField(default='',max_length=100)
    funded = BooleanField(default=False)
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:1]
    def initial(self): return self.name[len(object.name)-4:]
    def name_trimmed(self): return self.name[1:]
    def trim(self): return self.name.replace(" ","")
    def month(self): return locale[self.date.month-1]
    def elapsed(self): delta = self.start_time.date()-date.today(); return delta.days
    def deadline(self): delta = self.start_time.date()-self.end_time.date(); return delta.days
    def remaining(self): delta = self.end_time.date()-date.today(); return delta.days
    
class Interest(Model):
    key = CharField(default='',max_length=25)
    project = ForeignKey(Project)
    
class Movement(Model):
    name = CharField(max_length=50)
    user = ForeignKey(User,related_name='+')
    cause = ForeignKey(Project,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name[2:]
    def month(self): return locale[self.date.month-1]

class Pledge(Model):
    name = CharField(default='$#',max_length=10)
    value = IntegerField(default=1)
    backer = ForeignKey(User,related_name='backer')
    project = ForeignKey(Project,related_name='project')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def month(self): return locale[self.date.month-1]

class Event(Sellable):
    description = TextField(default='',max_length=500)
    deadline = DateTimeField(default=date.today())
    location = CharField(default='',max_length=200)
    event_id = CharField(default='',max_length=50)
    visual = CharField(default='',max_length=150)
    max = IntegerField(default=10)
    min = IntegerField(default=2)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name[2:]
    def month(self): return locale[self.date.month-1]
    def remaining(self): delta = self.deadline.date()-date.today(); return delta.days

class Ticket(Model):
    name = CharField(default='$@',max_length=10)
    value = IntegerField(default=1)
    buyer = ForeignKey(User,related_name='buyer')
    event = ForeignKey(Event,related_name='event')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def month(self): return locale[self.date.month-1]

