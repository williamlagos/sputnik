from django.db.models import ForeignKey,CharField,TextField,DateTimeField,IntegerField,BooleanField,Model
from django.contrib.auth.models import User
from datetime import date

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

class Causable(Model):
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
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def trim(self): return self.name.replace(" ","")
    def month(self): return locale[self.date.month-1]
    def remaining(self):
        delta = self.end_time.date()-date.today()
        return delta.days
    
class Keyword(Model):
    key = CharField(default='',max_length=25)
    project = ForeignKey(Causable)
    
class Movement(Model):
    name = CharField(max_length=50)
    user = ForeignKey(User,related_name='+')
    cause = ForeignKey(Causable,related_name='+')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]

class CausableDonated(Model):
    name = CharField(default='$#',max_length=10)
    value = IntegerField(default=1)
    donator = ForeignKey(User,related_name='donator')
    cause = ForeignKey(Causable,related_name='cause')
    date = DateTimeField(auto_now_add=True)
    def token(self): return self.name[:2]
    def month(self): return locale[self.date.month-1]