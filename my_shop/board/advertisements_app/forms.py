from django import forms
from .models import *


class CheckoutForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)



