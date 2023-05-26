from django.urls import path
from . import views


app_name = "ShopAPP"

urlpatterns = [    
      
      path('ProductDetails/<pid>'                       ,views.ProductDetails         ,name='ProductDetails')
     ,path('ModalProductDetails/<pid>'                  ,views.ModalProductDetails    ,name='ModalProductDetails')
     ,path('AddProduct/<pid>'                           ,views.AddProduct             ,name='AddProduct')
     ,path('AddWishProduct/<pid>'                       ,views.AddWishProduct         ,name='AddWishProduct')
     ,path('RemoveProduct/<pid>'                        ,views.RemoveProduct          ,name='RemoveProduct')
     ,path('DeleteProduct/<pid>'                        ,views.DeleteProduct          ,name='DeleteProduct')
     ,path('AddProducts/<pid>/<pnum>'                   ,views.AddProducts            ,name='AddProducts')
     ,path('Products/'                                  ,views.Products               ,name='Products')
     ,path('CosmeticsProducts/'                         ,views.CosmeticsProducts      ,name='CosmeticsProducts')
     ,path('ClothesProducts/'                           ,views.ClothesProducts        ,name='ClothesProducts')
     ,path('AccessoriesProducts/'                       ,views.AccessoriesProducts    ,name='AccessoriesProducts')
     ,path('ShowCartDetails/'                           ,views.ShowCartDetails        ,name='ShowCartDetails')
     ,path('ShoppingDetails/'                           ,views.ShoppingDetails        ,name='ShoppingDetails')
     ,path('WhishList/'                                 ,views.WhishList              ,name='WhishList')
     ,path('RemoveAll/'                                 ,views.RemoveAll              ,name='RemoveAll')
     ,path('SearchProduct/<category>/<searchWord>'      ,views.SearchProduct          ,name='SearchProduct')
     ,path('WishList/'                                  ,views.WishList               ,name='WishList')
     

    # ,path('follow'          ,views.follow  ,name='follow')CosmeticsProducts

    
   
]