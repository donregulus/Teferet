from django.shortcuts import render

# Create your views here.


def placeOrder(request):
    return render(request, 'OrderAPP/PlaceOrder.html')



def paypalPayment(request):
    return render(request, 'OrderAPP/PaypalPayment.html')



def creditCardPayment(request):
    return render(request, 'OrderAPP/CreditCardPayment.html')