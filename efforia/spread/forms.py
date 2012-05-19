from django.forms import Form,CharField,ModelForm
from django.forms.widgets import Textarea
from models import Event

class SpreadForm(Form):
	content = CharField(label="",widget=Textarea({'rows':10,'cols':50}))

class EventForm(ModelForm):
	class Meta:
		model = Event
		exclude = ('user','id_event','rsvp_status','date')
