#!/usr/bin/python
# -*- coding: utf-8 -*-
import json,time
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse as response
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import payment_was_successful
from paypal import fretefacil
from datetime import datetime

from correios import Correios
from core.models import Profile
from core.views import *
from models import Cart,Product,Deliverable
from forms import *

class Cancel(Efforia):
    def __init__(self): pass
    def cancel(self,request):
        u = self.current_user(request)
        Cart.objects.all().filter(user=u).delete()
        self.redirect('/')
        #value = int(self.request.arguments['credit'])
        #self.current_user().profile.credit -= value
        #self.current_user().profile.save()

class Payments(Efforia):
    def __init__(self): pass
    def view_recharge(self,request):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "1.19",
            "item_name": "Créditos do Efforia",
            "invoice": "unique-invoice-id",
            "notify_url": "http://www.efforia.com.br/paypal",
            "return_url": "http://www.efforia.com.br/",
            "cancel_return": "http://www.efforia.com.br/cancel",
            'currency_code': 'BRL',
            'quantity': '1'
        }
        payments = PayPalPaymentsForm(initial=paypal_dict)
        form = CreditForm()
        return render(request,"recharge.jade",{'form':payments,'credit':form},content_type='text/html')
    def update_credit(self,request):
        value = int(request.POST['credit'][0])
        current_profile = Profile.objects.all().filter(user=self.current_user(request))[0]
        if value > current_profile.credit: return self.view_recharge(request)
        else:
            current_profile.credit -= value
            current_profile.save()
            if 'other' in request.POST:
                iden = int(request.POST['other'][0])
                u = User.objects.all().filter(id=iden)[0]
                p = Profile.objects.all().filter(user=u)[0]
                p.credit += value
                p.save()
            self.accumulate_points(1,request)
            return response('')

class Mail(Efforia,Correios):
    def __init__(self): pass
    def postal_code(self,request):
        u = self.current_user(request)
        s = ''; mail_code = request.GET['address']
        q = self.consulta(mail_code)[0]
        d = fretefacil.create_deliverable('91350-180',mail_code,'30','30','30','0.5')
        value = fretefacil.delivery_value(d)
        formatted = '<div>Valor do frete: R$ <div style="display:inline;" class="delivery">%s</div></div>' % value 
        for i in q.values(): s += '<div>%s\n</div>' % i
        s += formatted
        now,objs,rels = self.get_object_bydate(request.GET['object'],'$$')
        obj = globals()[objs].objects.all().filter(date=now)[0]
        deliverable = Deliverable(product=obj,buyer=u,mail_code=mail_code,code=d['sender'],receiver=d['receiver'],
        height=int(d['height']),length=int(d['length']),width=int(d['width']),weight=int(float(d['weight'][0])*1000.0),value=value)
        deliverable.save()
        return response(s)

class Deliveries(Efforia):
    def __init__(self): pass
    def view_package(self,request):
        u = self.current_user(request)
        form = DeliveryForm()
        form.fields['address'].label = 'CEP'
        if 'quantity' in request.GET:
            quantity = request.GET['quantity']
            credit = int(request.GET['credit'])
        else:
            quantity = 1; credit = 1
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "1.00",
            "item_name": "Produto do Efforia",
            "invoice": "unique-invoice-id",
            "notify_url": "http://www.efforia.com.br/paypal",
            "return_url": "http://www.efforia.com.br/delivery",
            "cancel_return": "http://www.efforia.com.br/cancel",
            'currency_code': 'BRL',
            'quantity': quantity,
        }
        payments = PayPalPaymentsForm(initial=paypal_dict)
        diff = credit-u.profile.credit
        if diff < 0: diff = 0
        return render(request,"delivery.jade",{
                                               'payments':payments,
                                               'credit':diff,
                                               'form':form
                                               },content_type='text/html')
    def create_package(self,request):
        u = self.current_user(request)
        Cart.objects.all().filter(user=u).delete()
        return self.redirect('/')

class Carts(Efforia):
    def __init__(self): pass
    def view_cart(self,request):
        u = self.current_user(request)
        quantity = 0; value = 0;
        cart = list(Cart.objects.all().filter(user=u))
        for c in cart: 
            quantity += c.quantity
            value += c.product.credit*c.quantity
        #if len(cart): cart.insert(0,Action('buy',{'quantity':quantity,'value':value}))
        #else: cart.insert(0,Action('create'))
        return self.render_grid(cart,request)
    def add_tocart(self,request):
        u = self.current_user(request)
        strp_time = request.POST['time']
        now = datetime.strptime(strp_time,"%Y-%m-%d %H:%M:%S.%f")
        prod = Product.objects.all().filter(date=now)[0]
        exists = Cart.objects.all().filter(user=u,product=prod)
        if not len(exists): 
            cart = Cart(user=u,product=prod)
            cart.save()
        else: 
            exists[0].quantity += 1
            exists[0].save()
        quantity = 0; value = 0;
        cart = list(Cart.objects.all().filter(user=u))
        for c in cart: 
            quantity += c.quantity
            value += c.product.credit*c.quantity
        #cart.insert(0,Action('buy',{'quantity':quantity,'value':value}))
        return self.render_grid(cart,request)

class Store(Efforia):
    def __init__(self): pass
    def view_product(self,request):
        u = self.current_user(request)
        if 'action' in request.GET:
            deliver = list(Deliverable.objects.all().filter(buyer=u))
            #deliver.insert(0,Action('products'))
            if not len(deliver) or 'more' in request.GET:
                products = list(Product.objects.all())
                #products.insert(0,Action('create'))
                return self.render_grid(list(products),request)
            else: return self.render_grid(deliver,request)
        elif 'product' in request.GET:
            date = request.GET['product']
            now = datetime.strptime(date[0],"%Y-%m-%d %H:%M:%S.%f")
            prod = Product.objects.all().filter(date=now)[0]
            self.srender('product.html',product=prod)
        else:
            return render(request,'product.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
        
    def create_product(self,request):
        category=request.POST['category'][0]
        credit=request.POST['credit'][0]
        visual=request.POST['visual'][0]
        name=request.POST['name'][0]
        description=request.POST['description'][0]
        product = Product(category=category,credit=credit,visual=visual,
                          name='&'+name,description=description,seller=self.current_user(request))
        product.save()
        return response('Produto criado com sucesso!',content_type='text/plain')

#payment_was_successful.connect(confirm_payment)
