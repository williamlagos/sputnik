#!/usr/bin/python
# -*- coding: utf-8 -*-
from django_pagseguro.pagseguro import CarrinhoPagSeguro,ItemPagSeguro
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render 
from django.conf import settings

class PagSeguro:
    def process(self,request):
    	for k,v in request.REQUEST.iteritems():
	    if 'product' in k: product = v
	    elif 'value' in k: value = float(v)
	    elif 'qty' in k: qty = int(v)
        #carrinho.set_cliente(email='oi@efforia.com.br',cep='91350180')
        carrinho = CarrinhoPagSeguro(ref_transacao=1)
        carrinho.add_item(ItemPagSeguro(cod=1,descr=product,quant=qty,valor=value))
        form_pagseguro = carrinho.form()
        return render(request,'form.jade',{'form':form_pagseguro})

class PayPal:
    def process(self,request):
    	for k,v in request.REQUEST.iteritems():
	    if 'product' in k: product = v
	    elif 'value' in k: value = float(v)
	    elif 'qty' in k: qty = int(v)
        paypal = {
            'business':      settings.PAYPAL_RECEIVER_EMAIL,
            'notify_url':    settings.PAYPAL_NOTIFY_URL,
            'return_url':    settings.PAYPAL_RETURN_URL,
            'cancel_return': settings.PAYPAL_CANCEL_RETURN,
            'invoice':       'unique-invoice-id',
            'currency_code': 'BRL',
        }
        paypal['amount'] = str(value)
        paypal['item_name'] = product
        paypal['quantity'] = str(qty)
        form_paypal = PayPalPaymentsForm(initial=paypal)
	return render(request,'form.jade',{'form':form_paypal.render()})

class Baskets:
    def view_items(self,request):
        u = self.current_user(request)
        quantity = 0; value = 0;
        cart = list(Cart.objects.all().filter(user=u))
        for c in cart: 
            quantity += c.quantity
            value += c.product.credit*c.quantity
        #if len(cart): cart.insert(0,Action('buy',{'quantity':quantity,'value':value}))
        #else: cart.insert(0,Action('create'))
        return self.render_grid(cart,request)
    def add_item(self,request):
        u = self.current_user(request)
        id = request.REQUEST['id']
        prod = globals()['Product'].objects.all().filter(id=id)[0]
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
