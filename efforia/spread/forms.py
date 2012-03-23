from django.forms import Form,CharField

class FriendSearch(Form):
    name = CharField(label="")

class SpreadForm(Form):
    content = CharField(label="")
