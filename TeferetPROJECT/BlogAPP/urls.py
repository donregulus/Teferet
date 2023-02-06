from django.urls import path
from . import views


app_name = "BlogAPP"

urlpatterns = [
        
     path(''             ,views.Blog        ,name='Blog')
    ,path('BlogDetails/' ,views.BlogDetails ,name='BlogDetails')
    ,path('SendComment/' ,views.SendComment ,name='SendComment')
     

    # ,path('follow'          ,views.follow  ,name='follow')
   
]