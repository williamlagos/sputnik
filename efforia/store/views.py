#!/usr/bin/python
# -*- coding: utf-8 -*-
from paypal.standard.forms import PayPalPaymentsForm
from paypal import fretefacil
from tornado.template import Template
from datetime import datetime
from handlers import append_path
append_path()

import time

from core.correios import Correios
from spread.views import SocialHandler,Action
from models import Cart,Product,Deliverable
from forms import *

class PaymentHandler(SocialHandler):
    def get(self):
        # What you want the button to do.
        paypal_dict = {
            "business": "caokzu@gmail.com",
            "amount": "1.19",
            "item_name": "Créditos do Efforia",
            "invoice": "unique-invoice-id",
            "notify_url": "http://www.efforia.com.br/your-ipn-location/",
            "return_url": "http://www.efforia.com.br/your-return-location/",
            "cancel_return": "http://www.efforia.com.br/your-cancel-location/",
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
        self.write(str(q))

class DeliveryHandler(SocialHandler):
    def get(self):
        form = DeliveryForm()
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