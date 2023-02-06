from django.shortcuts import render, redirect
from django.contrib.auth.models import User



from UserAuthsAPP.models import UserProfile
# Create your views here.



def ProductDetails(request):   

    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                }       
        return render(request, 'ShopAPP/ProductDetails.html',context)
    else:   
        return render(request, 'ShopAPP/ProductDetails.html')



def Products(request):   

    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                }       
        return render(request, 'ShopAPP/Products.html',context)
    else:   
        return render(request, 'ShopAPP/Products.html')    
