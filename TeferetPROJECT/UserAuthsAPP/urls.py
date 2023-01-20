from django import views
from django.urls import path
from UserAuthsAPP import views


urlpatterns = [
    
     path(''                ,views.Register   ,name='sign-up')
    # ,path('follow'          ,views.follow  ,name='follow')
   
]