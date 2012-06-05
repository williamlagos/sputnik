#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import Form,IntegerField

class CreditForm(Form):
    credits = IntegerField()
