from django.urls import path
from . import views


app_name = "OrderAPP"

urlpatterns = [         
     
     path('PaypalPayment/'          ,views.PaypalPayment      ,name='PaypalPayment')
    ,path('CreditCardPayment/'      ,views.CreditCardPayment  ,name='CreditCardPayment')
    ,path('SuccessPayment/'         ,views.SuccessPayment     ,name='SuccessPayment')
    ,path('CancelPayment/'          ,views.CancelPayment      ,name='CancelPayment')
    
     
     

    # ,path('follow'          ,views.follow  ,name='follow')
   
]