from django.urls import path
from . import views


app_name = "ShopAPP"

urlpatterns = [    
      
      path('ProductDetails/<pid>'     ,views.ProductDetails       ,name='ProductDetails')
     ,path('ModalProductDetails/<pid>',views.ModalProductDetails  ,name='ModalProductDetails')
     ,path('AddProduct/<pid>'         ,views.AddProduct           ,name='AddProduct')
     ,path('Products/'                ,views.Products             ,name='Products')
     ,path('CosmeticsProducts/'       ,views.CosmeticsProducts    ,name='CosmeticsProducts')
     ,path('ClothesProducts/'         ,views.ClothesProducts      ,name='ClothesProducts')
     ,path('AccessoriesProducts/'     ,views.AccessoriesProducts  ,name='AccessoriesProducts')
     ,path('ShowCartDetails/'         ,views.ShowCartDetails      ,name='ShowCartDetails')
     

    # ,path('follow'          ,views.follow  ,name='follow')CosmeticsProducts
   
]