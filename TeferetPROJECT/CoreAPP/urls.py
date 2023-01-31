from django.urls import path
from . import views


app_name = "CoreAPP"

urlpatterns = [
    
      path(''                ,views.index   ,name='index')
     ,path('Contact/'                ,views.contact   ,name='Contact')
     ,path('About/'                ,views.about   ,name='About')

    # ,path('follow'          ,views.follow  ,name='follow')
   
]