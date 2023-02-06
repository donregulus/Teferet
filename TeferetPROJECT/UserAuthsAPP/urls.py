from django import views
from django.urls import path
from UserAuthsAPP import views


app_name = "UserAuthsAPP"

urlpatterns = [
    
     path('Register'                            ,views.Register           ,name='Register')
    ,path('Login'                               ,views.Login              ,name='Login')
    ,path('ForgotPassword'                      ,views.ForgotPassword     ,name='ForgotPassword')
    ,path('EmailResetPassword/<uidb64>/<token>/', views.EmailResetPassword,name='EmailResetPassword')
    ,path('ResetPassword'                       ,views.ResetPassword      ,name='ResetPassword')
    ,path('Logout'                              ,views.Logout             ,name='Logout')
    ,path('DashBoard'                           ,views.DashBoard          ,name='DashBoard')



    
    # ,path('follow'          ,views.follow  ,name='follow')
   
]