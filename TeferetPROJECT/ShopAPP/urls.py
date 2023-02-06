from django.urls import path
from . import views


app_name = "ShopAPP"

urlpatterns = [    
      
      path('ProductDetails/'          ,views.ProductDetails   ,name='ProductDetails')
     ,path('Products/'                ,views.Products         ,name='Products')
     

    # ,path('follow'          ,views.follow  ,name='follow')
   
]