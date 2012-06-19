from django.db.models import ForeignKey,CharField,TextField,IntegerField,FloatField,DateTimeField,Model
from django.contrib.auth.models import User
from datetime import date

class Product(Model):
    name = CharField(default='',max_length=150)
    seller = ForeignKey(User,related_name='+')
    category = IntegerField(default=1)
    description = TextField()
    credit = IntegerField(default=5)
    visual = CharField(default='',max_length=40)
    date = DateTimeField(default=date.today(),auto_now_add=True)
    
class Cart(Model):
    name = CharField(default='++',max_length=2)
    quantity = IntegerField(default=1)
    user = ForeignKey(User,related_name='+')
    product = ForeignKey(Product,related_name='+')
    
class Deliverable(Model):
    product = ForeignKey(Product,related_name='+')
    buyer = ForeignKey(User,related_name='+')
    code = CharField(default='',max_length=50)
    mail_code = CharField(default='',max_length=50)
    height = IntegerField(default=1)
    length = IntegerField(default=1)
    width = IntegerField(default=1)
    weight = IntegerField(default=10)
    receiver = CharField(default='',max_length=50)
    value = FloatField(default=0.0)
    