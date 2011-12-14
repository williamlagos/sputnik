from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import SpreadForm,RegisterForm
from models import Spread,UserProfile

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            newuser = form.registerUser()
            profile = UserProfile(user=newuser,age=form.data['age'])
            profile.save()
            return HttpResponseRedirect(reverse('core.views.profile')) # Redirect after POST
    else:
        form = RegisterForm() # An unbound form
    return render_to_response('registration/register.html',{'form': form,})

@login_required
def spread(request):
    if request.method == 'POST':
        form = SpreadForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('core.views.spreads'))
    else:
        form = SpreadForm()
    return render_to_response('spread.html',{'form': form,})

def spreads(request):
    #spreads = Spread.objects.get(user=request.user)
    spreads = Spread.objects.all()
    return render_to_response('list.html',locals(),
                              context_instance=RequestContext(request))

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except:
        return HttpResponseRedirect("register/") 
    return render_to_response('home.html',locals(),
                              context_instance=RequestContext(request))  