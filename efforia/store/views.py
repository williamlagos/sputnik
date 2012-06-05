#!/usr/bin/python
# -*- coding: utf-8 -*-
from paypal.standard.forms import PayPalPaymentsForm
from handlers import append_path
append_path()

from spread.views import SocialHandler
from forms import CreditForm

class PaymentHandler(SocialHandler):
    def get(self):
        # What you want the button to do.
        paypal_dict = {
            "business": "caokzu@gmail.com",
            "amount": "1.07",
            "item_name": "Créditos do Efforia",
            "invoice": "unique-invoice-id",
            "notify_url": "http://www.efforia.com.br/your-ipn-location/",
            "return_url": "http://www.efforia.com.br/your-return-location/",
            "cancel_return": "http://www.efforia.com.br/your-cancel-location/",
            'currency_code': 'BRL'
        }
        payments = PayPalPaymentsForm(initial=paypal_dict)
        form = CreditForm()
        return self.srender("payment.html",form=payments,credit=form)