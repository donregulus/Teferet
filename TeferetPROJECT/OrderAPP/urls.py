from django.urls import path
from . import views


app_name = "OrderAPP"

urlpatterns = [         
     
     path('CreditCardPayment/'                 ,views.CreditCardPayment    ,name='CreditCardPayment')
    ,path('RegisterOrderPayment/<paymentMode>' ,views.RegisterOrderPayment ,name='RegisterOrderPayment')
    ,path('CancelPayment/'                     ,views.CancelPayment        ,name='CancelPayment')
    ,path('SuccessPayment/'                    ,views.SuccessPayment       ,name='SuccessPayment')
    
     
     

    # ,path('follow'          ,views.follow  ,name='follow')
   
]