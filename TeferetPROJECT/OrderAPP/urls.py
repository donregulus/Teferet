from django.urls import path
from . import views


app_name = "OrderAPP"

urlpatterns = [    
      
     path('PlaceOrder/'             ,views.PlaceOrder         ,name='PlaceOrder')
    ,path('PaypalPayment/'          ,views.PaypalPayment      ,name='PaypalPayment')
    ,path('CreditCardPayment/'      ,views.CreditCardPayment  ,name='CreditCardPayment')
     
     

    # ,path('follow'          ,views.follow  ,name='follow')
   
]