from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from ShopAPP.models import Cart, CartItem, Product
from ShopAPP.views import __cart_id__
from django.core import serializers

# Create your views here.








    


@login_required(login_url="UserAuthsAPP:Login")
def PaypalPayment(request):
    return render(request, 'OrderAPP/PaypalPayment.html')


@login_required(login_url="UserAuthsAPP:Login")
def CreditCardPayment(request):
    return render(request, 'OrderAPP/CreditCardPayment.html')