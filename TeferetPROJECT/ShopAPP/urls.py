from django.urls import path
from . import views


app_name = "ShopAPP"

urlpatterns = [    
      
      path('ProductDetails/'          ,views.productDetails   ,name='ProductDetails')
     ,path('Products/'                ,views.products         ,name='Products')
     

    # ,path('follow'          ,views.follow  ,name='follow')
   
]