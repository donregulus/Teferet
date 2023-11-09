from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.core import serializers
from django.conf import settings
from django.urls import  reverse





from ShopAPP.models import Cart, CartItem, Product,Variation
from OrderAPP.models import Order


import stripe
import json



stripe.api_key = 'sk_test_VePHdqKTYQjKNInc7u56JBrQ'

YOUR_DOMAIN = 'http://localhost:8000'


def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required(login_url="UserAuthsAPP:Login")
def CreditCardPayment(request):

    cart_items = []
    items = []          

    urlBase = request.build_absolute_uri()    
    urlBase = urlBase.replace(request.get_full_path(), "")    

    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)      
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)    
            cart_items = CartItem.objects.all().filter(cart=cart)
    total = 0
    for item in cart_items:     
        total += item.product.price       
        finalItem = {
                        "price_data" : {
                                            'currency': 'usd',
                                            'product_data': {
                                                            'name': item.product.name,
                                                            },
                                            'unit_amount': int(item.product.price*100),#conversion from cent to dollar
                                        },
                        "quantity" : item.quantity            
                    }
        items.append(finalItem)
 
    session = stripe.checkout.Session.create(
    line_items=items,
    mode='payment',
    success_url= urlBase + '/Order/CreditCardSuccess?session_id={CHECKOUT_SESSION_ID}',
    cancel_url = urlBase + '/Order/CancelPayment',
    
  )
    return redirect(session.url, code=303)
    


def CreditCardSuccess(request):
  session = stripe.checkout.Session.retrieve(request.GET['session_id'])
  total = session.amount_total/100 #conversion from cent to dollar
  return redirect("OrderAPP:RegisterOrderPayment",paymentMode="CreditCard",totalAmout=total)


@login_required(login_url="UserAuthsAPP:Login")
def RegisterOrderPayment(request,paymentMode,totalAmout):  
    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)    

        #Get The User IP address
        ip = get_ip_address(request)

        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)

            #update stocks
            cart_items = CartItem.objects.all().filter(cart=cart)
            for item in cart_items:
                if len(item.variation.strip()) == 0:                    
                    #Update  the product stock                    
                    item.product.stock -= item.quantity
                    item.product.save()
                else:
                    #Update  the variation product quantity
                    productVariation = Variation.objects.get(product=item.product,variation_value=item.variation)
                    productVariation.quantity -= item.quantity
                    productVariation.save()
                    
                    #Update  the product stock                    
                    item.product.stock -= item.quantity
                    item.product.save()

            cart.isActive=False   
            cart.save()         
            #Save Order
            if(paymentMode == "PayPal"):
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)                
                id = body['id']
                status = body['status']

                order = Order.objects.create(user=LoggedUser,cart=cart,PaymentMode="PayPal",userIpAddress=ip,PaymentStatus=status,providerOrderId=id,totalAmout=totalAmout)
                order.save()            
            elif(paymentMode == "CreditCard"):            
                order = Order.objects.create(user=LoggedUser,cart=cart,PaymentMode="CreditCard",totalAmout=totalAmout,PaymentStatus="COMPLETED")
                order.save()
            
    return render(request, 'OrderAPP/Success.html')


@login_required(login_url="UserAuthsAPP:Login")
def CancelPayment(request):  
    return render(request, 'OrderAPP/Cancel.html')


@login_required(login_url="UserAuthsAPP:Login")
def SuccessPayment(request):  
    return render(request, 'OrderAPP/Success.html')

@login_required(login_url="UserAuthsAPP:Login")
def ViewOrders(request):
    #Get The current user
    LoggedUser = User.objects.get(username=request.user)   

    #Get current user orders
    orders = Order.objects.filter(user=LoggedUser)
    ordersParsed = []
    for item in orders:
        lDeliveredStatus=str()
        match item.DeliveredStatus:
             case 1:
                lDeliveredStatus = "IN PREPARATION"
             case 2:
                lDeliveredStatus = "IN DELIVERY"
             case 3:
                lDeliveredStatus = "RECEIVED"
        itemParsed = {"details":item,"status":lDeliveredStatus}
        ordersParsed.append(itemParsed)

    context = {                    
                        "OrderList": ordersParsed,
                    }
    return render(request, 'OrderAPP/ViewOrders.html',context)

@login_required(login_url="UserAuthsAPP:Login")
def ViewOrderDetails(request,pid):    
    #Get order
    order = Order.objects.get(id=pid)

    #Get the cartItems related to the order
    cartItems = CartItem.objects.filter(cart=order.cart)

    context = {                    
                        "Products": cartItems,
                        "Total": order.totalAmout,
                    }
    return render(request, 'OrderAPP/ViewOrderDetails.html',context)