from django.shortcuts import render, redirect
from django.contrib.auth.models import User



from UserAuthsAPP.models import UserProfile
from ShopAPP.models import Product, Category, Cart, CartItem
# Create your views here.


from django.core import serializers
import json


from django.http import HttpResponse


def __cart_id__(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def __isAjax__(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True
    else:
        return False

def ModalProductDetails(request,pid):
    product = Product.objects.get(pid=pid)
    context = {                    
                    "product" : product,
                }         
    return render(request, 'ShopAPP/ModalProductDetails.html',context)

def ProductDetails(request,pid):   

    product = Product.objects.get(pid=pid)
    context = {                    
                    "product" : product,
                }     
    
    if __isAjax__(request):    
            productDetails = {
                "image": product.image.url,
                "price": str(product.price),
                "name" : product.name
            }            
            return HttpResponse(json.dumps(productDetails))
    else:            
            return render(request, 'ShopAPP/ProductDetails.html',context)
    
def Products(request):  
    products = Product.objects.all()
    context = {                   
                    "products": products,
                }       
    return render(request, 'ShopAPP/Products.html',context)    

def CosmeticsProducts(request):
    Cosmetics = Category.objects.get(name="Cosmetics")
    products = Product.objects.filter(Category=Cosmetics.cid)
    context = {                    
                    "products": products,
                }   
    return render(request, 'ShopAPP/CosmeticsProducts.html',context)

def ClothesProducts(request):
    Cosmetics = Category.objects.get(name="Clothes")
    products = Product.objects.filter(Category=Cosmetics.cid)    
    context = {                    
                    "products": products,
                }   
    return render(request, 'ShopAPP/ClothesProducts.html',context)

def AccessoriesProducts(request):
    Cosmetics = Category.objects.get(name="Accessories")
    products = Product.objects.filter(Category=Cosmetics.cid)
   
    context = {                    
                    "products": products,
                }   
    return render(request, 'ShopAPP/AccessoriesProducts.html',context)

def ShowCartDetails(request):

    cart_items = []
    totalPrice = 0

    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)    
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)    
            cart_items = CartItem.objects.all().filter(cart=cart)
    else:
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,cartid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,cartid=__cart_id__(request))
            cart_items = CartItem.objects.all().filter(cart=cart)
        

    for item in cart_items:
        totalPrice += item.sub_total()

    cart_items_json = serializers.serialize('json', cart_items)    
    res = {
        "total": str(totalPrice),
        "items": cart_items_json,
    }
    return HttpResponse(json.dumps(res))


def AddProduct(request,pid):

    Itemscount = 0
    cart_item  =  None

    #get the product
    product = Product.objects.get(pid=pid)
    
    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)    
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)
        else:         
            cart = Cart.objects.create(user=LoggedUser)
            cart.save()
         
        #Check If item to add is already in cart
        cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
        if cartItemExist : 
            item = CartItem.objects.get(cart=cart,product=product)
            item.quantity +=1
            item.save()
            cart_items = CartItem.objects.all().filter(cart=cart)
        else:
            item = CartItem.objects.create(cart=cart,product=product,quantity=1)
            item.save()        
            cart_items = CartItem.objects.all().filter(cart=cart)

    else:        
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,cartid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,cartid=__cart_id__(request))
        else:         
            cart = Cart.objects.create(cartid=__cart_id__(request))
            cart.save()            
        #Check If item to add is already in cart
        cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
        if cartItemExist : 
            item = CartItem.objects.get(cart=cart,product=product)
            item.quantity +=1
            item.save()
            cart_items = CartItem.objects.all().filter(cart=cart)
        else:
            item = CartItem.objects.create(cart=cart,product=product,quantity=1)
            item.save()        
            cart_items = CartItem.objects.all().filter(cart=cart)
    
    for cart_item in cart_items:
        Itemscount += cart_item.quantity
    
    return HttpResponse(Itemscount)