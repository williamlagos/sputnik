from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import SpreadForm,FriendSearch
from models import Spread,UserProfile

@login_required
def spread(request):
    if request.method == 'POST':
        form = SpreadForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('core.views.spreads'))
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
            friend = form.searchUser()
            return HttpResponseRedirect(reverse('core.views.people'))
    else:
        form = FriendSearch()
    return render_to_response('search.html',locals(),
                              context_instance=RequestContext(request))

@login_required
def people(request):
    users = UserProfile.objects.all()
    return render_to_response('people.html',locals(),
                              context_instance=RequestContext(request))