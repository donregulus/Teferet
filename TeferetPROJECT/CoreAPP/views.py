from django.shortcuts import render



from UserAuthsAPP.models import UserProfile
from ShopAPP.models import Product

# Create your views here.
def Index(request):

    products = Product.objects.all()
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        print(products)
        context = {
                    "userProfile": LoggedUserProfile,
                    "products": products,
                }   
        return render(request, "CoreAPP/Index.html",context)
    else:
        context = {                    
                    "products": products,
                }   
        return render(request, "CoreAPP/Index.html",context)


def Contact(request):
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                }   
        return render(request, "CoreAPP/Contact.html",context)
    else:
        return render(request, "CoreAPP/Contact.html")


def About(request):
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                }   
        return render(request, "CoreAPP/About.html",context)
    else:
        return render(request, "CoreAPP/About.html")