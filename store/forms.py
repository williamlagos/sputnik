#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import ModelForm,Form,IntegerField
from models import Product,Deliverable

class CreditForm(Form):
    credits = IntegerField()

class DeliveryForm(ModelForm):
    class Meta:
        model = Deliverable
        exclude = ('buyer','code','height','length','width','weight','receiver','product')

class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('seller')