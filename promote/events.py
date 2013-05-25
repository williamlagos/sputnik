from efforia.main import Efforia
from django.shortcuts import render
from django.http import HttpResponse as response
from django.conf import settings
from datetime import timedelta,date
from models import Event
from efforia.models import Sellable
from efforia.files import Dropbox

class Events(Efforia):
    def __init__(self): pass
    def view_event(self,request):
        return render(request,'event.jade',{},content_type='text/html')
    def promote_event(self,request):
        event_id = int(request.GET['id'])
        e = Event.objects.filter(id=event_id)[0]
        t = Sellable.objects.filter(sellid=event_id)
        return render(request,'eventview.jade',{'title':e.name[2:],'location':e.location.encode('utf-8'),
        'event':e,'ratio':len(t)/e.max,'buyers':len(t),'remaining':e.remaining},content_type='text/html')
    def create_event(self,request):
        u = self.current_user(request)
        title = descr = local = max = min = value = dates = ''
        for k,v in request.REQUEST.iteritems():
            if 'name' in k: title = v
            elif 'description' in k: descr = v
            elif 'location' in k: local = v
            elif 'deadline' in k: dates = v
            elif 'max' in k: max = v
            elif 'min' in k: min = v
            elif 'value' in k: value = v
        date = self.convert_datetime(dates)
        Event(name='@@%s'%title,user=u,deadline=date,description=descr,
        max=max,min=min,value=value,location=local).save()
        return render(request,'eventimage.jade',{'static_url':settings.STATIC_URL})
    def event_image(self,request):
        u = self.current_user(request)
        photo = request.FILES['Filedata'].read()
        dropbox = Dropbox()
        link = dropbox.upload_and_share(photo)
        res = self.url_request(link)
        e = list(Event.objects.filter(user=u))[0]
        e.visual = '%s?dl=1' % res
        e.save()
        return response(e.visual)
    def show_enroll(self,request):
        u = self.current_user(request)
        event = Event.objects.filter(user=u,id=request.REQUEST['id'])[0]
        return render(request,'enroll.jade',{'static_url':settings.STATIC_URL,'value':event.value})
    def event_id(self,request):
        u = self.current_user(request)
        e = list(Event.objects.filter(user=u))[0]
        e.event_id = request.REQUEST['id']
        e.save()
        return response('Event created successfully')
