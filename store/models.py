from django.db.models import ForeignKey,CharField,TextField,IntegerField,FloatField,DateTimeField,Model
from django.contrib.auth.models import User
from datetime import date

locale = ('Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez')

class Product(Model):
    name = CharField(default='',max_length=150)
    seller = ForeignKey(User,related_name='+')
    category = IntegerField(default=1)
    description = TextField()
    credit = IntegerField(default=5)
    visual = CharField(default='',max_length=40)
    date = DateTimeField(default=date.today(),auto_now_add=True)
    def token(self): return self.name[:1]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def real_month(self): return locale[self.date.month-1]
    
class Cart(Model):
    name = CharField(default='++',max_length=2)
    quantity = IntegerField(default=1)
    user = ForeignKey(User,related_name='+')
    product = ForeignKey(Product,related_name='+')
    def token(self): return self.name[:2]
    def total_value(self): return self.quantity*self.product.credit
    def product_trimmed(self): return self.product.name_trimmed()
    def product_month(self): return self.product.real_month()
    
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
    date = DateTimeField(default=date.today(),auto_now_add=True)
    def token(self): return self.name[:2]
    def name_trimmed(self): return self.name.split(';')[0][1:]
    def month(self): return locale[self.date.month-1]
    
