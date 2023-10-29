from django.shortcuts import render


from django.contrib.auth.models import User
from UserAuthsAPP.models import UserProfile
from ShopAPP.models import Product, WhishList

# Create your views here.
def Index(request):
    products = Product.objects.all().order_by('-createdDate')[:8]
    if request.user.is_authenticated:

        productsWithWish = list()
        #get the current logged user
        LoggedUser = User.objects.get(username=request.user)    

        #get  all products

        for product in products:
            #Check If item is  in WishList
            wishItemExist   =  WhishList.objects.all().filter(user=LoggedUser,product=product).exists()
            if wishItemExist :
                item ={
                    "wish": True,
                    "details": product,
                }
                productsWithWish.append(item)
            else:
                item ={
                    "wish": False,
                    "details": product,
                }
                productsWithWish.append(item)

        context = {                    
                        "products": productsWithWish,
                    }   
        return render(request, "CoreAPP/Index.html",context)
        
    else:        
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