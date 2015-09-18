#!/usr/bin/python
# -*- coding: utf-8 -*-
from social import Search,Follows,ID,Deletes,Authentication,Twitter,Facebook,Tutorial,Coins
from control import Profiles,Passwords,Control,Places,Photos
from feed import Mosaic,Pages
from main import Efforia
from payments import PagSeguro,PayPal,Baskets
from models import Sellable

def profileview(request,name='me'):
    e = Efforia()
    if request.method == 'GET':
        return e.profile_view(request,name)

def basket(request):
    b = Baskets()
    if request.method == 'GET':
        return b.view_items(request)
    elif request.method == 'POST':
        return b.add_item(request)

def basketclean(request):
    b = Baskets()
    if request.method == 'GET':
        return b.clean_basket(request)

def pagseguro(request):
    p = PagSeguro()
    if request.method == 'GET':
        return p.process(request)

def pagsegurocart(request):
    p = PagSeguro()
    if request.method == 'GET':
        return p.process_cart(request)

def paypal(request):
    p = PayPal()
    if request.method == 'GET':
        return p.process(request)

def paypalcart(request):
    p = PayPal()
    if request.method == 'GET':
        return p.process_cart(request)

def discharge(request):
    c = Coins()
    if request.method == 'GET':
        c.discharge(request)

def recharge(request):
    c = Coins()
    if request.method == 'GET':
        c.recharge(request)

def balance(request):
    c = Coins()
    if request.method == 'GET':
        c.balance(request)

def payment(request):
    pay = Coins()
    if request.method == 'GET':
        return pay.view_recharge(request)
    elif request.method == 'POST':
        return pay.update_credit(request)

def pageview(request):
    p = Pages()
    if request.method == 'GET':
        return p.page_view(request)
    
def pageedit(request):
    p = Pages()
    if request.method == 'GET':
        return p.edit_page(request)
    elif request.method == 'POST':
        return p.save_page(request)

def page(request):
    p = Pages()
    if request.method == 'GET':
        return p.view_page(request)
    elif request.method == 'POST':
        return p.create_page(request)

def search(request):
    s = Search()
    if request.method == 'GET':
        return s.explore(request)

def explore(request):
    p = Profiles()
    if request.method == 'GET':
        return p.view_userinfo(request)

def mosaic(request):
    m = Mosaic()
    if request.method == 'GET':
        return m.view_mosaic(request)

def activity(request):
    p = Profiles()
    if request.method == 'GET':
        return p.view_activity(request)

def deadlines(request):
    m = Mosaic()
    if request.method == 'GET':
        return m.deadlines(request)

def following(request):
    fav = Follows()
    if request.method == 'GET':
        return fav.view_following(request)

def follow(request):
    f = Follows()
    if request.method == 'GET':
        return f.become_follower(request)

def unfollow(request):
    f = Follows()
    if request.method == 'GET':
        return f.leave_follower(request)

def main(request):
    e = Efforia()
    if request.method == 'GET':
        return e.start(request)
    elif request.method == 'POST':
        return e.external(request)

def ids(request):
    i = ID()
    if request.method == 'GET':
        return i.view_id(request)
    elif request.method == 'POST':
        return i.finish_tutorial(request)

def delete(request):
    d = Deletes()
    if request.method == 'GET':
        return d.delete_element(request)

def profile(request):
    prof = Profiles()
    if request.method == 'GET':
        return prof.view_profile(request)
    elif request.method == 'POST':
        return prof.update_profile(request)

def place(request):
    p = Places()
    if request.method == 'GET':
        return p.register_place(request)
    elif request.method == 'POST':
        return p.create_place(request)

def password(request):
    pasw = Passwords()
    if request.method == 'GET':
        return pasw.view_password(request)
    elif request.method == 'POST':
        return pasw.change_password(request)

def photo(request):
    p = Photos()
    if request.method == 'GET':
        return p.view_photo(request)
    elif request.method == 'POST':
        return p.change_photo(request)

def appearance(request):
    c = Control()
    if request.method == 'GET':
        return c.view_control(request)
    elif request.method == 'POST':
        return c.change_control(request)

def options(request):
    c = Control()
    if request.method == 'GET':
        return c.view_options(request)

def config(request):
    c = Control()
    if request.method == 'GET':
        return c.view_panel(request)

def integrations(request):
    c = Control()
    if request.method == 'GET':
        return c.view_integrations(request)

def authenticate(request):
    a = Authentication()
    if request.method == 'GET':
        return a.authenticate(request)

def leave(request):
    a = Authentication()
    if request.method == 'GET':
        return a.leave(request)

def twitter_post(request):
    t = Twitter()
    if request.method == 'GET':
        return t.update_status(request)

def facebook_post(request):
    f = Facebook()
    if request.method == 'GET':
        return f.update_status(request)

def facebook_event(request):
    f = Facebook()
    if request.method == 'GET':
        return f.send_event(request)
    
def facebook_eventcover(request):
    f = Facebook()
    if request.method == 'GET':
        return f.send_event_cover(request)
    
def participate(request):
    a = Authentication()
    if request.method == 'GET':
        return a.view_register(request)
    elif request.method == 'POST':
        return a.participate(request)

def tutorial(request):
    t = Tutorial()
    if request.method == 'GET':
        return t.view_tutorial(request)
    elif request.method == 'POST':
        return t.finish_tutorial(request)
