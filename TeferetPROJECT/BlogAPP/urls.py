from django.urls import path
from . import views


app_name = "BlogAPP"

urlpatterns = [
        
     path(''            ,views.blog        ,name='Blog')
    ,path('BlogDetails/' ,views.blogDetails ,name='BlogDetails')
     

    # ,path('follow'          ,views.follow  ,name='follow')
   
]