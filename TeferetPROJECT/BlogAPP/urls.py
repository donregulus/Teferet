from django.urls import path
from . import views


app_name = "BlogAPP"

urlpatterns = [
        
     path(''                  ,views.Blogs        ,name='Blog')
    ,path('BlogDetails/<bid>' ,views.BlogDetails ,name='BlogDetails')
    ,path('SendComment/'      ,views.SendComment ,name='SendComment')
     
   
]