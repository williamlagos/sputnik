"""hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include#, url
from django.contrib import admin
from django.views.generic import TemplateView
from django_distill import distill_url as url
from sputnik.views import *

def getNone():
    return None

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls), distill_func=getNone),
    # url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="home", distill_func=getNone),
    # url(r'^vantagens/', AdvantagesPageView.as_view(), name='advantages', distill_func=getNone),
    # url(r'^produtos/', PricingPageView.as_view(), name='pricing', distill_func=getNone),
    # url(r'^parceiros/', PartnersPageView.as_view(), name='partners', distill_func=getNone),
    # url(r'^contato/', ContactPageView.as_view(), name='contact', distill_func=getNone)
]
