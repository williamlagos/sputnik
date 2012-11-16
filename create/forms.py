from django.forms import Form,CharField
from django.forms.widgets import Textarea

class CausesForm(Form):
    title = CharField(label="")
    content = CharField(label="",widget=Textarea({'rows':8,'cols':30}))