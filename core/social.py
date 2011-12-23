from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import SpreadForm,FriendSearch
from models import Spread,UserProfile
from django.contrib.auth.models import User

@login_required
def spread(request):
    if request.method == 'POST':
        form = SpreadForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('core.social.spreads'))
    else:
        form = SpreadForm()
    return render_to_response('spread.html', locals(),
                              context_instance=RequestContext(request))
        
@login_required
def spreads(request):
    spreads = Spread.objects.all().filter(user=request.user)
    return render_to_response('spreads.html', locals(),
                              context_instance=RequestContext(request))

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except:
        return HttpResponseRedirect("register/") 
    return render_to_response('home.html',locals(),
                              context_instance=RequestContext(request))  

@login_required
def search(request): 
    if request.method == 'POST':
        form = FriendSearch(request.POST)
        if form.is_valid(): 
            friends = form.searchUser()
            profiles = UserProfile.objects.all()
            return render_to_response('people.html',locals(),
                              context_instance=RequestContext(request))
    else:
        form = FriendSearch()
    return render_to_response('search.html',locals(),
                              context_instance=RequestContext(request))

@login_required
def people(request):
    friends = User.objects.all()
    profiles = UserProfile.objects.all()
    return render_to_response('people.html',locals(),
                              context_instance=RequestContext(request))