from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import PostForm,RegisterForm
from models import Post,UserProfile

@login_required
def spread(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('core.views.spreader'))
    return render_to_response('spread.html',locals(),
                              context_instance=RequestContext(request))

def spreader(request):
    posts = Post.objects.all()
    return render_to_response('list.html',locals(),
                              context_instance=RequestContext(request))
    
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
def profile(request):
    try:
        profile = request.user.profile
    except:
        pass
        #return HttpResponseRedirect("register/") 
    return render_to_response('home.html',locals(),
                              context_instance=RequestContext(request))  