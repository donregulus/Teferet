from django.urls import path
from . import views


app_name = "ShopAPP"

urlpatterns = [    
      
      path('ProductDetails/<pid>'     ,views.ProductDetails       ,name='ProductDetails')
     ,path('ModalProductDetails/<pid>',views.ModalProductDetails  ,name='ModalProductDetails')
     ,path('Products/'                ,views.Products             ,name='Products')
     ,path('CosmeticsProducts/'       ,views.CosmeticsProducts    ,name='CosmeticsProducts')
     ,path('ClothesProducts/'         ,views.ClothesProducts      ,name='ClothesProducts')
     ,path('AccessoriesProducts/'     ,views.AccessoriesProducts  ,name='AccessoriesProducts')
     

    # ,path('follow'          ,views.follow  ,name='follow')CosmeticsProducts
   
]