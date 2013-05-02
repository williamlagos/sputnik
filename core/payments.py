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
