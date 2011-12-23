from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

def playvideo(request):
    return render_to_response('play.html', locals(),
                              context_instance=RequestContext(request))