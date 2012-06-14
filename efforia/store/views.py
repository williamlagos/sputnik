#!/usr/bin/python
# -*- coding: utf-8 -*-
from paypal.standard.forms import PayPalPaymentsForm
from tornado.template import Template
from handlers import append_path
append_path()

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

class ProductsHandler(SocialHandler):
    def get(self):
        if 'action' in self.request.arguments:
            form = ProductCreationForm()
            return self.render_form(form,'products','Criar um novo produto')
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