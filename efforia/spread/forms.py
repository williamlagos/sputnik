from django.forms import Form,CharField
from django.forms.widgets import Textarea

class SpreadForm(Form):
    content = CharField(label="")
    
class CausesForm(Form):
    title = CharField(label="")
    content = CharField(label="",widget=Textarea)
