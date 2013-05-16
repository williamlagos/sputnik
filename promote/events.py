from efforia.main import Efforia
from django.shortcuts import render
from django.http import HttpResponse as response
from models import Event

class Events(Efforia):
    def __init__(self): pass
    def view_event(self,request):
        return render(request,'event.jade',{},content_type='text/html')
    def promote_event(self,request):
        event_id = int(request.GET['id'])
        e = Event.objects.filter(id=event_id)[0]
        return render(request,'eventview.jade',{'title':e.name,'location':e.location.encode('utf-8'),'eventid':event_id},content_type='text/html')
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
        return response('Event created successfully')

