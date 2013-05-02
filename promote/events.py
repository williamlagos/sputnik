from core.main import Efforia
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
        name = request.POST['name']
        local = request.POST['location']
        times = request.POST['start_time'],request.POST['end_time']
        dates = []
        for t in times: dates.append(self.convert_datetime(t))
        event_obj = Event(name='@@'+name,user=self.current_user(request),start_time=dates[0],
                          end_time=dates[1],location=local,id_event='',rsvp_status='')
        event_obj.save()
        self.accumulate_points(1,request)
        return response('Event created successfully')

