from django.forms import Form,CharField
from django.forms.widgets import Textarea

class SpreadForm(Form):
    content = CharField(label="",widget=Textarea({'rows':10,'cols':50}))