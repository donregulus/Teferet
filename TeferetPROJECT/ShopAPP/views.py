from django.shortcuts import render, redirect
from django.contrib.auth.models import User



from UserAuthsAPP.models import UserProfile
from ShopAPP.models import Product, Category
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


def CosmeticsProducts(request):
    Cosmetics = Category.objects.get(name="Cosmetics")
    products = Product.objects.filter(Category=Cosmetics.cid)
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        print(products)
        context = {
                    "userProfile": LoggedUserProfile,
                    "products": products,
                }   
        return render(request, "CoreAPP/CosmeticsProducts.html",context)
    else:   
        context = {                    
                    "products": products,
                }   
        return render(request, 'ShopAPP/CosmeticsProducts.html',context)
    
def ClothesProducts(request):
    Cosmetics = Category.objects.get(name="Clothes")
    products = Product.objects.filter(Category=Cosmetics.cid)
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        print(products)
        context = {
                    "userProfile": LoggedUserProfile,
                    "products": products,
                }   
        return render(request, "CoreAPP/ClothesProducts.html",context)
    else:   
        context = {                    
                    "products": products,
                }   
        return render(request, 'ShopAPP/ClothesProducts.html',context)
    

def AccessoriesProducts(request):
    Cosmetics = Category.objects.get(name="Accessories")
    products = Product.objects.filter(Category=Cosmetics.cid)
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        print(products)
        context = {
                    "userProfile": LoggedUserProfile,
                    "products": products,
                }   
        return render(request, "CoreAPP/AccessoriesProducts.html",context)
    else:   
        context = {                    
                    "products": products,
                }   
        return render(request, 'ShopAPP/AccessoriesProducts.html',context)