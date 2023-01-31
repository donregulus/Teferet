from django.urls import path
from . import views


app_name = "OrderAPP"

urlpatterns = [    
      
     path('PlaceOrder/'             ,views.placeOrder      ,name='PlaceOrder')
    ,path('PaypalPayment/'          ,views.paypalPayment      ,name='PaypalPayment')
    ,path('CreditCardPayment/'          ,views.creditCardPayment      ,name='CreditCardPayment')
     
     

    # ,path('follow'          ,views.follow  ,name='follow')
   
]