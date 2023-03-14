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


def Search(request):    
    searchword = str()    
    if request.method=="POST":
        searchword = request.POST["search"]
        product_list = Product.objects.filter(name__icontains=searchword)        
    context = {'product_list':product_list,"searchword":searchword}
    return render(request, "CoreAPP/Search.html",context)    


def Contact(request):   
    return render(request, "CoreAPP/Contact.html")


def About(request):
    return render(request, "CoreAPP/About.html")