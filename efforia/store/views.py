#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import payment_was_successful
from paypal import fretefacil
from django.conf import settings
from tornado.template import Template
from datetime import datetime
from coronae import append_path
from tornado.httpclient import *
from tornado.httputil import *
import logging,tornado.web
append_path()

import time

from core.correios import Correios
from core.models import Profile
from core.views import *
from models import Cart,Product,Deliverable
from forms import *

class CancelHandler(Efforia):
    def post(self):
        Cart.objects.all().filter(user=self.current_user()).delete()
        self.redirect('/')
        #value = int(self.request.arguments['credit'])
        #self.current_user().profile.credit -= value
        #self.current_user().profile.save()

class PaypalIpnHandler(tornado.web.RequestHandler):
    def post(self):
        """Accepts or rejects a Paypal payment notification."""
        input = self.request.arguments # remember to decode this! you could run into errors with charsets!
        if 'txn_id' in input and 'verified' in input['payer_status'][0]:
            pass
        else:
            raise HTTPError(402)

class PaymentHandler(Efforia):
    def get(self):
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
        return self.srender("payment.html",form=payments,credit=form)
    def post(self):
        value = int(self.request.arguments['credit'][0])
        current_profile = Profile.objects.all().filter(user=self.current_user)[0]
        if value > current_profile.credit: self.write('Créditos insuficientes.');
        else:
            current_profile.credit -= value
            current_profile.save()
            if 'other' in self.request.arguments:
                iden = int(self.request.arguments['other'][0])
                print iden
                u = User.objects.all().filter(id=iden)[0]
                p = Profile.objects.all().filter(user=u)[0]
                p.credit += value
                p.save()
            self.accumulate_points(1)
            self.write('')

class CorreiosHandler(Efforia,Correios):
    def get(self):
        s = ''; mail_code = self.request.arguments['address'][0]
        q = self.consulta(mail_code)[0]
        d = fretefacil.create_deliverable('91350-180',mail_code,'30','30','30','0.5')
        value = fretefacil.delivery_value(d)
        formatted = '<div>Valor do frete: R$ <div style="display:inline;" class="delivery">%s</div></div>' % value 
        for i in q.values(): s += '<div>%s\n</div>' % i
        s += formatted
        now,objs,rels = self.get_object_bydate(self.request.arguments['object'][0],'$$')
        obj = globals()[objs].objects.all().filter(date=now)[0]
        deliverable = Deliverable(product=obj,buyer=self.current_user(),mail_code=mail_code,code=d['sender'],receiver=d['receiver'],
        height=int(d['height']),length=int(d['length']),width=int(d['width']),weight=int(float(d['weight'][0])*1000.0),value=value)
        deliverable.save()
        self.write(s)

class DeliveryHandler(Efforia):
    def get(self):
        form = DeliveryForm()
        form.fields['address'].label = 'CEP'
        quantity = self.request.arguments['quantity'][0]
        credit = int(self.request.arguments['credit'][0])
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
        diff = credit-self.current_user().profile.credit
        if diff < 0: diff = 0
        return self.srender("delivery.html",payments=payments,credit=diff,form=form)
    def post(self):
        print self.request.arguments
        Cart.objects.all().filter(user=self.current_user()).delete()
        self.redirect('/')
    def create_package(self):
        pass

class CartHandler(Efforia):
    def get(self):
        quantity = 0; value = 0;
        cart = list(Cart.objects.all().filter(user=self.current_user()))
        for c in cart: 
            quantity += c.quantity
            value += c.product.credit*c.quantity
        if len(cart): cart.insert(0,Action('buy',{'quantity':quantity,'value':value}))
        else: cart.insert(0,Action('moreproducts'))
        self.render_grid(cart)
    def post(self):
        strp_time = self.request.arguments['time'][0]
        now = datetime.strptime(strp_time,"%Y-%m-%d %H:%M:%S.%f")
        prod = Product.objects.all().filter(date=now)[0]
        exists = Cart.objects.all().filter(user=self.current_user(),product=prod)
        if not len(exists): 
            cart = Cart(user=self.current_user(),product=prod)
            cart.save()
        else: 
            exists[0].quantity += 1
            exists[0].save()
        quantity = 0; value = 0;
        cart = list(Cart.objects.all().filter(user=self.current_user()))
        for c in cart: 
            quantity += c.quantity
            value += c.product.credit*c.quantity
        cart.insert(0,Action('buy',{'quantity':quantity,'value':value}))
        self.render_grid(cart)

class ProductsHandler(Efforia):
    def get(self):
        if 'action' in self.request.arguments:
            form = ProductCreationForm()
            form.fields['name'].label = 'Nome do produto'
            form.fields['category'].label = 'Categoria'
            form.fields['description'].label = ''
            form.fields['description'].initial = 'Descreva aqui, de uma forma breve, o produto que você irá adicionar ao Efforia.'
            form.fields['credit'].label = 'Valor (Em créditos)'
            form.fields['visual'].label = 'Ilustração'
            return self.render_form(form,'products','Criar um novo produto')
        elif 'product' in self.request.arguments:
            date = self.request.arguments['product']
            now = datetime.strptime(date[0],"%Y-%m-%d %H:%M:%S.%f")
            prod = Product.objects.all().filter(date=now)[0]
            self.srender('product.html',product=prod)
        else:
            deliver = list(Deliverable.objects.all().filter(buyer=self.current_user))
            deliver.insert(0,Action('products'))
            if not len(deliver) or 'more' in self.request.arguments:
                products = list(Product.objects.all())
                products.insert(0,Action('create'))
                return self.render_grid(list(products))
            else: return self.render_grid(deliver)
    def post(self):
        category=self.request.arguments['category'][0]
        credit=self.request.arguments['credit'][0]
        visual=self.request.arguments['visual'][0]
        name=self.request.arguments['name'][0]
        description=self.request.arguments['description'][0]
        product = Product(category=category,credit=credit,visual=visual,
                          name='&'+name,description=description,seller=self.current_user())
        product.save()
        self.write('Produto criado com sucesso!')

#payment_was_successful.connect(confirm_payment)