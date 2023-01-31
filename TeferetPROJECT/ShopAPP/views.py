from django.shortcuts import render

# Create your views here.



def productDetails(request):
    return render(request, 'ShopAPP/ProductDetails.html')



def products(request):
    return render(request, 'ShopAPP/Products.html')    
