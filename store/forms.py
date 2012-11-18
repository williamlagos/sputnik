#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import ModelForm,Form,IntegerField,CharField
from models import Product,Deliverable

class CreditForm(Form):
    credits = IntegerField()

class DeliveryForm(Form):
    address = CharField(max_length=10)

class ProductCreationForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('seller')