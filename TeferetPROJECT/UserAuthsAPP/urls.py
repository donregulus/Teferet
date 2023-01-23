from django import views
from django.urls import path
from UserAuthsAPP import views


app_name = "UserAuthsAPP"

urlpatterns = [
    
     path('Register'                ,views.Register   ,name='Register')
    ,path('Login'           ,views.Login  ,name='Login')
    # ,path('follow'          ,views.follow  ,name='follow')
   
]