from django.urls import path
from . import views


app_name = "CoreAPP"

urlpatterns = [
    
      path(''                ,views.Index   ,name='Index')
     ,path('Contact/'        ,views.Contact ,name='Contact')
     ,path('About/'          ,views.About   ,name='About')
     ,path('Search/'         ,views.Search  ,name='Search')

    # ,path('follow'          ,views.follow  ,name='follow')
   
]