#!/usr/bin/python
# -*- coding: utf-8 -*-
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import payment_was_successful
from paypal import fretefacil
from django.conf import settings
from tornado.template import Template
from datetime import datetime
from handlers import append_path
from tornado.httpclient import *
from tornado.httputil import *
import logging,tornado.web
append_path()

import time

from core.correios import Correios
from core.models import Profile
from spread.views import SocialHandler,Action
from models import Cart,Product,Deliverable
from forms import *

class PaypalIpnHandler(tornado.web.RequestHandler):
    def post(self):
        """Accepts or rejects a Paypal payment notification."""
        input = self.request.arguments # remember to decode this! you could run into errors with charsets!
        if 'txn_id' in input and 'verified' in input['payer_status'][0]:
            pass
        else:
            raise HTTPError(402)

class PaymentHandler(SocialHandler):
    def get(self):
        # What you want the button to do.
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

class CorreiosHandler(SocialHandler,Correios):
    def get(self):
        mail_code = self.request.arguments['mail_code'][0]
        q = self.consulta(mail_code)[0]
        d = fretefacil.create_deliverable('91350-180',mail_code,'30','30','30','0.5')
        q['frete'] = fretefacil.delivery_value(d)
#        paypal_dict = {
#            "business": "caokzu@gmail.com",
#            "amount": "1.19",
#            "item_name": "Créditos do Efforia",
#            "invoice": "unique-invoice-id",
#            "notify_url": "http://www.efforia.com.br/your-ipn-location/",
#            "return_url": "http://www.efforia.com.br/your-return-location/",
#            "cancel_return": "http://www.efforia.com.br/your-cancel-location/",
#            'currency_code': 'BRL',
#            'quantity': '1'
#        }
#        payments = PayPalPaymentsForm(initial=paypal_dict)
#        form = CreditForm()
        s = ''
        q['frete'] += 'reais'
        for i in q.values(): s += '%s\n' % i
        self.write(s)

class DeliveryHandler(SocialHandler):
    def get(self):
        form = DeliveryForm()
        form.fields['mail_code'].label = 'Código Postal'
        form.fields['value'].label = 'Valor'
        credit = self.request.arguments['credit'][0]
        form.fields['value'].initial = '%s Créditos' % credit#,float(credit)*1.19)
        self.render_form(form,'delivery','Confirmar compra')

class CartHandler(SocialHandler):
    def get(self):
        quantity = 0; value = 0;
        cart = list(Cart.objects.all().filter(user=self.current_user()))
        for c in cart: 
            quantity += c.quantity
            value += c.product.credit*c.quantity
        cart.insert(0,Action('buy',{'quantity':quantity,'value':value}))
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
        self.write('Added products on cart')

class ProductsHandler(SocialHandler):
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
            deliver = Deliverable.objects.all().filter(buyer=self.current_user)
            if not len(deliver):
                products = list(Product.objects.all())
                products.insert(0,Action('create'))
                return self.render_grid(list(products))
            else: return self.render_grid(deliver)
#            #sched = Schedule.objects.all(); feed = []
#            #for s in sched.values('name').distinct(): feed.append(sched.filter(name=s['name'],user=self.current_user())[0])
#            feed = []; feed.append(Action('abc'))
#            play = Playable.objects.all().filter(user=self.current_user())
#            for p in play: feed.append(p)
#            self.render_grid(feed)
#        elif 'view' in self.request.arguments:
#            name = self.request.arguments['title'][0]; play = []
#            sched = Schedule.objects.all().filter(user=self.current_user,name='>>'+name) 
#            for s in sched: play.append(s.play)
#            self.srender('grid.html',feed=play,number=len(play))
#        else:
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