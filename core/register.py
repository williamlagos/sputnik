from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import UserProfile
from forms import RegisterForm

def newuser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            newuser = form.registerUser()
            profile = UserProfile(user=newuser,age=form.data['age'])
            profile.save()
            return HttpResponseRedirect(reverse('core.social.profile')) # Redirect after POST
    else:
        form = RegisterForm() # An unbound form
    return render_to_response('registration/register.html',{'form': form,})
