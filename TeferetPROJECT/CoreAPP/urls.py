from django.urls import path
from . import views


app_name = "CoreAPP"

urlpatterns = [
    
      path(''                ,views.Index   ,name='Index')
     ,path('Contact/'        ,views.Contact ,name='Contact')
     ,path('About/'          ,views.About   ,name='About')

    # ,path('follow'          ,views.follow  ,name='follow')
   
]