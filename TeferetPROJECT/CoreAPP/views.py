from django.shortcuts import render



from UserAuthsAPP.models import UserProfile
from ShopAPP.models import Product

# Create your views here.
def Index(request):
    products = Product.objects.all()  
    context = {                    
                    "products": products,
                }   
    return render(request, "CoreAPP/Index.html",context)


def Contact(request):   
    return render(request, "CoreAPP/Contact.html")


def About(request):
    return render(request, "CoreAPP/About.html")