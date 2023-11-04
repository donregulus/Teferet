from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Min, Max
from django.template.loader import render_to_string
from django.http import HttpResponse,JsonResponse
from django.core import serializers
import json
import uuid

from UserAuthsAPP.models import UserProfile
from ShopAPP.models import Product, Category, Cart, CartItem, WhishList
# Create your views here.


def __cart_id__(request):    

    if not request.user.is_authenticated:
        cartSession = request.session.session_key
        if not cartSession:
                request.session.save()              
                cartSession = request.session.session_key
        return cartSession
    else:
        cartSession = request.session.session_key
         #Get The current user
        LoggedUser = User.objects.get(username=request.user)
        if Cart.objects.filter(isActive=True,sessionid=cartSession,user=LoggedUser).exists():
            cartSession = request.session.create()    
        if request.session.get("logout") == True :
            cartSession = request.session.create()    
            request.session["logout"]= False     
        else:  
            if not cartSession:
                cartSession = request.session.create()            
        return cartSession

def __isAjax__(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True
    else:
        return False

def ModalProductDetails(request,pid):
        
    quantity = 0
    product = Product.objects.get(pid=pid)
    ProductImages = product.productAllImages.all()
    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)    
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)    
            cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
            if cartItemExist:
                quantity = CartItem.objects.get(cart=cart,product=product).quantity

    else:
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request))            
            #Check If item to add is already in cart
            cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
            if cartItemExist:
                quantity = CartItem.objects.get(cart=cart,product=product).quantity        
    
    context = {                    
                    "product" : product,
                    "quantity": quantity,
                     "ProductImages":ProductImages
                }         
    return render(request, 'ShopAPP/ModalProductDetails.html',context)

def ProductDetails(request,pid):   

    quantity = 0
    product = Product.objects.get(pid=pid)    
    RelatedProducts = Product.objects.filter(Category=product.Category).exclude(pid=pid).order_by('-createdDate')[:8]
    ProductImages = product.productAllImages.all()
    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)    
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)    
            cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
            if cartItemExist:
                quantity = CartItem.objects.get(cart=cart,product=product).quantity

    else:
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request),user=None).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request),user=None)            
            #Check If item to add is already in cart
            cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
            if cartItemExist:
                quantity = CartItem.objects.get(cart=cart,product=product).quantity        
    
    context = {                    
                    "product" : product,
                    "quantity": quantity,
                    "ProductImages":ProductImages,
                    "RelatedProducts":RelatedProducts
                }           
    
    if __isAjax__(request):    
            productDetails = {
                "image": product.image.url,
                "price": str(product.price),
                "name" : product.name,
                "quantity": str(quantity),
            }            
            return HttpResponse(json.dumps(productDetails))
    else:            
            return render(request, 'ShopAPP/ProductDetails.html',context)
    
def Products(request):  

    #get  all products
    products = Product.objects.all().order_by('-createdDate')
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    colorsAvaillable = []
    colors =  Product.objects.values('color').distinct()
    for item in colors:
        match item["color"] :
            case 1:
                colorsAvaillable.append({"color":"#0f0f0f","name":"Black","id":1})                
            case 2:
                colorsAvaillable.append({"color":"#BA2828","name":"Red","id":2})
            case 3:
                colorsAvaillable.append({"color":"#317034","name":"Green","id":3})
            case 4:
                colorsAvaillable.append({"color":"#F5E23D","name":"Yellow","id":4})
            case 5:
                colorsAvaillable.append({"color":"#1D6CBA","name":"Blue","id":5})
            case 6:
                colorsAvaillable.append({"color":"#EFEFEF","name":"White","id":6})    

    if request.user.is_authenticated:

        productsWithWish = list()
        #get the current logged user
        LoggedUser = User.objects.get(username=request.user)    

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

        page = request.GET.get("page")
        paginator = Paginator(productsWithWish, 8)     
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)        
        context = {                  
                        "products": posts,
                        "url":"/Shop/Products",
                        "min_max_price":min_max_price,
                        "cid":"all",
                        "colorsAvaillable":colorsAvaillable,
                        
                    }
        if request.htmx:
            return render(request, 'ShopAPP/Partials/PartialProductsList.html',context)  
        return render(request, 'ShopAPP/Products.html',context)
        
    else:        
        page = request.GET.get("page")
        paginator = Paginator(products, 8)        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {                  
                        "products": posts,
                        "url":"/Shop/Products",
                        "min_max_price":min_max_price,
                        "cid":"all",
                        "colorsAvaillable":colorsAvaillable,
                    }
        if request.htmx:
            return render(request, 'ShopAPP/Partials/PartialProductsList.html',context)      
        return render(request, 'ShopAPP/Products.html',context)    

def CosmeticsProducts(request):
    Cosmetics = Category.objects.get(name="Cosmetics")
    products = Product.objects.filter(Category=Cosmetics.cid).order_by('-createdDate')
    min_max_price = Product.objects.filter(Category=Cosmetics.cid).aggregate(Min("price"), Max("price"))
    
    colorsAvaillable = []
    colors =  Product.objects.filter(Category=Cosmetics.cid).values('color').distinct()
    for item in colors:
        match item["color"] :
            case 1:
                colorsAvaillable.append({"color":"#0f0f0f","name":"Black","id":1})                
            case 2:
                colorsAvaillable.append({"color":"#BA2828","name":"Red","id":2})
            case 3:
                colorsAvaillable.append({"color":"#317034","name":"Green","id":3})
            case 4:
                colorsAvaillable.append({"color":"#F5E23D","name":"Yellow","id":4})
            case 5:
                colorsAvaillable.append({"color":"#1D6CBA","name":"Blue","id":5})
            case 6:
                colorsAvaillable.append({"color":"#EFEFEF","name":"White","id":6})  

    if request.user.is_authenticated:
        productsWithWish = list()
        LoggedUser = User.objects.get(username=request.user)    

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

        page = request.GET.get("page")
        paginator = Paginator(productsWithWish, 4)     
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)        
        context = {                  
                        "products": posts,
                        "url":"/Shop/CosmeticsProducts",
                        "min_max_price":min_max_price,
                        "cid":Cosmetics.cid,
                        "colorsAvaillable":colorsAvaillable,
                    }
        if request.htmx:
            return render(request, 'ShopAPP/Partials/PartialProductsList.html',context)  
        return render(request, 'ShopAPP/CosmeticsProducts.html',context)
        
    else:                
        page = request.GET.get("page")
        paginator = Paginator(products, 4)        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {                  
                        "products": posts,
                        "url":"/Shop/CosmeticsProducts",
                        "min_max_price":min_max_price,
                        "cid":Cosmetics.cid,
                        "colorsAvaillable":colorsAvaillable,
                    }
        if request.htmx:
            return render(request, 'ShopAPP/Partials/PartialProductsList.html',context)      
        return render(request, 'ShopAPP/CosmeticsProducts.html',context)

def ClothesProducts(request):    
    Clothes = Category.objects.get(name="Clothes")
    products = Product.objects.filter(Category=Clothes.cid).order_by('-createdDate')
    min_max_price = Product.objects.filter(Category=Clothes.cid).aggregate(Min("price"), Max("price"))

    colorsAvaillable = []
    colors =  Product.objects.filter(Category=Clothes.cid).values('color').distinct()
    for item in colors:
        match item["color"] :
            case 1:
                colorsAvaillable.append({"color":"#0f0f0f","name":"Black","id":1})                
            case 2:
                colorsAvaillable.append({"color":"#BA2828","name":"Red","id":2})
            case 3:
                colorsAvaillable.append({"color":"#317034","name":"Green","id":3})
            case 4:
                colorsAvaillable.append({"color":"#F5E23D","name":"Yellow","id":4})
            case 5:
                colorsAvaillable.append({"color":"#1D6CBA","name":"Blue","id":5})
            case 6:
                colorsAvaillable.append({"color":"#EFEFEF","name":"White","id":6})  
    if request.user.is_authenticated:

        productsWithWish = list()
        #get the current logged user
        LoggedUser = User.objects.get(username=request.user)    

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

        page = request.GET.get("page")
        paginator = Paginator(productsWithWish, 4)     
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)        
        context = {                  
                        "products": posts,
                        "url":"/Shop/ClothesProducts",
                        "min_max_price":min_max_price,
                        "cid":Clothes.cid,
                        "colorsAvaillable":colorsAvaillable,
                    }
        if request.htmx:
            return render(request, 'ShopAPP/Partials/PartialProductsList.html',context)  
        return render(request, 'ShopAPP/ClothesProducts.html',context)
        
    else:      
        page = request.GET.get("page")
        paginator = Paginator(products, 4)        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {                  
                        "products": posts,
                        "url":"/Shop/ClothesProducts",
                        "min_max_price":min_max_price,
                        "cid":Clothes.cid,
                        "colorsAvaillable":colorsAvaillable,
                    }
        if request.htmx:
            return render(request, 'ShopAPP/Partials/PartialProductsList.html',context)                  
        return render(request, 'ShopAPP/ClothesProducts.html',context)

def AccessoriesProducts(request):
    Accessories = Category.objects.get(name="Accessories")
    products = Product.objects.filter(Category=Accessories.cid).order_by('-createdDate')
    min_max_price = Product.objects.filter(Category=Accessories.cid).aggregate(Min("price"), Max("price"))

    colorsAvaillable = []
    colors =  Product.objects.filter(Category=Accessories.cid).values('color').distinct()
    for item in colors:
        match item["color"] :
            case 1:
                colorsAvaillable.append({"color":"#0f0f0f","name":"Black","id":1})                
            case 2:
                colorsAvaillable.append({"color":"#BA2828","name":"Red","id":2})
            case 3:
                colorsAvaillable.append({"color":"#317034","name":"Green","id":3})
            case 4:
                colorsAvaillable.append({"color":"#F5E23D","name":"Yellow","id":4})
            case 5:
                colorsAvaillable.append({"color":"#1D6CBA","name":"Blue","id":5})
            case 6:
                colorsAvaillable.append({"color":"#EFEFEF","name":"White","id":6})  

    if request.user.is_authenticated:
        productsWithWish = list()
        #get the current logged user
        LoggedUser = User.objects.get(username=request.user)    

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

        page = request.GET.get("page")
        paginator = Paginator(productsWithWish, 4)        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
                
        context = {                  
                        "products": posts,
                        "url":"/Shop/AccessoriesProducts",
                        "min_max_price":min_max_price,
                        "cid":Accessories.cid,
                        "colorsAvaillable":colorsAvaillable
                    }
        if request.htmx:
            return render(request, 'ShopAPP/Partials/PartialProductsList.html',context)
        return render(request, 'ShopAPP/AccessoriesProducts.html',context)     
    else:                
        page = request.GET.get("page")
        paginator = Paginator(products, 4)        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {                  
                        "products": posts,
                        "url":"/Shop/AccessoriesProducts",
                        "min_max_price":min_max_price,
                        "cid":Accessories.cid,
                        "colorsAvaillable":colorsAvaillable,
                    }
        if request.htmx:
            return render(request, 'ShopAPP/Partials/PartialProductsList.html',context)
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
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request),user=None).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request),user=None)
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
            cart = Cart.objects.create(user=LoggedUser,sessionid=__cart_id__(request))
            cart.save()
         
        #Check If item to add is already in cart
        cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
        if cartItemExist : 
            item = CartItem.objects.get(cart=cart,product=product)
            item.quantity += 1
            item.save()
            cart_items = CartItem.objects.all().filter(cart=cart)
        else:
            item = CartItem.objects.create(cart=cart,product=product,quantity=1)
            item.save()        
            cart_items = CartItem.objects.all().filter(cart=cart)

    else:        
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request),user=None).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request),user=None)
        else:         
            cart = Cart.objects.create(sessionid=__cart_id__(request))
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

def ShoppingDetails(request):  

    cart_items = []
    products = []
    totalPrice = 0
    UserLoggedProfile = None
        

    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)  
        UserLoggedProfile = UserProfile.objects.get(user=LoggedUser)        
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)    
            cart_items = CartItem.objects.all().filter(cart=cart)
    else:
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request),user=None).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request),user=None)
            cart_items = CartItem.objects.all().filter(cart=cart)
        

    
    if __isAjax__(request):
        for item in cart_items:
            totalPrice += item.sub_total()        
            finalItem = {
            "productName" : item.product.name,
            "productPrice" : str(item.product.price),
            "productId" : str(item.product.pid),
            "productImage" : item.product.image.url,
            "quantity" : item.quantity,
            "total": str(item.sub_total())
             }
            products.append(finalItem)

        context = {
        "total": str(totalPrice),
        "products": products,        
        } 
        return HttpResponse(json.dumps(context))
    else:
        for item in cart_items:
            totalPrice += item.sub_total()        
            finalItem = {
            "product" : item.product,
            "quantity" : item.quantity,
            "total": item.sub_total()
             }
            products.append(finalItem)

        context = {
        "total": str(totalPrice),
        "products": products,
        "UserLoggedProfile": UserLoggedProfile,
        }
        return render(request, 'ShopAPP/ShoppingDetails.html',context)
    
def RemoveAll(request):

    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)    
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)    
            cart.delete()
            return redirect("ShopAPP:ShoppingDetails")
    else:
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request),user=None).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request),user=None)
            cart.delete()
            return redirect("ShopAPP:ShoppingDetails")

def AddProducts(request,pid,pnum):
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
            item.quantity = int(pnum)
            item.save()
            cart_items = CartItem.objects.all().filter(cart=cart)
        else:
            item = CartItem.objects.create(cart=cart,product=product,quantity=1)
            item.save()        
            cart_items = CartItem.objects.all().filter(cart=cart)

    else:        
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request))
        else:         
            cart = Cart.objects.create(sessionid=__cart_id__(request))
            cart.save()            
        #Check If item to add is already in cart
        cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
        if cartItemExist : 
            item = CartItem.objects.get(cart=cart,product=product)
            item.quantity =int(pnum)
            item.save()
            cart_items = CartItem.objects.all().filter(cart=cart)
        else:
            item = CartItem.objects.create(cart=cart,product=product,quantity=1)
            item.save()        
            cart_items = CartItem.objects.all().filter(cart=cart)
    
    for cart_item in cart_items:
        Itemscount += cart_item.quantity
    return HttpResponse(Itemscount)

def RemoveProduct(request,pid):
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
            item.quantity -= 1
            item.save()
            cart_items = CartItem.objects.all().filter(cart=cart)       

    else:        
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request),user=None).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request),user=None)
        else:         
            cart = Cart.objects.create(sessionid=__cart_id__(request))
            cart.save()            
        #Check If item to add is already in cart
        cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
        if cartItemExist : 
            item = CartItem.objects.get(cart=cart,product=product)
            item.quantity -=1
            item.save()
            cart_items = CartItem.objects.all().filter(cart=cart)        
    
    for cart_item in cart_items:
        Itemscount += cart_item.quantity
    return HttpResponse(Itemscount)

def DeleteProduct(request,pid):
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
            item.delete()            
            cart_items = CartItem.objects.all().filter(cart=cart)   
            if len(cart_items) == 0:
                cart.delete()

    else:        
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,sessionid=__cart_id__(request),user=None).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=__cart_id__(request),user=None)
        else:         
            cart = Cart.objects.create(sessionid=__cart_id__(request))
            cart.save()            
        #Check If item to add is already in cart
        cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
        if cartItemExist : 
            item = CartItem.objects.get(cart=cart,product=product)            
            item.delete()
            cart_items = CartItem.objects.all().filter(cart=cart)  
            if len(cart_items) == 0:
                cart.delete()     
    
    for cart_item in cart_items:
        Itemscount += cart_item.quantity
    return HttpResponse(Itemscount)

def SearchProduct(request, category, searchWord):
    if request.method=="GET":
        product_list=[]
        if category == 'ALL':
            product_list = Product.objects.filter(name__icontains=searchWord)
        else:
            categoryObj = Category.objects.get(name=category)            
            product_list = Product.objects.filter(name__icontains=searchWord, Category=categoryObj.cid)
        products = []
        for item in product_list:            
            finalItem = {
            "productName" : item.name,
            "productPrice" : str(item.price),
            "productId" : str(item.pid),
            "productImage" : item.image.url,
            "category" : item.Category.name   
             }
            products.append(finalItem)
        return HttpResponse( json.dumps(products))

def FiltersProduct(request,cid):

    minPrice = request.GET["minPrice"]
    maxPrice = request.GET["maxPrice"]

    colorsTofilter = request.GET.getlist('color[]')


    products = None
    paginatorNumber = None

    if str(cid).strip()=="all":
        #get  all products
        paginatorNumber = 8
        products = Product.objects.all().order_by('-createdDate')
    else : 
        #get  products per category
        paginatorNumber = 4
        products = Product.objects.filter(Category=cid).order_by('-createdDate')

    #filter by color
    if len(colorsTofilter) > 0:
        products= products.filter(color__in=colorsTofilter).distinct()
    
    #filter by price
    products = products.filter(price__gte=minPrice)
    products = products.filter(price__lte=maxPrice)
    
    if request.user.is_authenticated:

        productsWithWish = list()
        #get the current logged user
        LoggedUser = User.objects.get(username=request.user)    

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

        page = request.GET.get("page")
        paginator = Paginator(productsWithWish, paginatorNumber)     
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)        
              
        data = render_to_string("ShopAPP/Partials/PartialProductsList.html",{"products":posts})
        return JsonResponse({"data":data})

        
    else:        
        page = request.GET.get("page")
        paginator = Paginator(products, paginatorNumber)        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        data = render_to_string("ShopAPP/Partials/PartialProductsList.html",{"products":posts})
        return JsonResponse({"data":data,"size":len(posts)})  


@login_required(login_url="UserAuthsAPP:Login")
def WishList(request):
    LoggedUser = User.objects.get(username=request.user)    
    UserWishList   =  WhishList.objects.all().filter(user=LoggedUser)
    wishListResponse = list()
    
    for whish in UserWishList:             
            finalItem = {
            "productName" : whish.product.name,
            "productId" : str(whish.product.pid),
            "productImage" : whish.product.image.url            
            }
            wishListResponse.append(finalItem)   
    if __isAjax__(request):
        return HttpResponse(json.dumps(wishListResponse))
    else:
        context = {        
        "WhishList": wishListResponse,        
        }
        return render(request, 'ShopAPP/WhishListDetails.html',context)

@login_required(login_url="UserAuthsAPP:Login")
def AddWishProduct(request,pid):
    wishCount = 0
    wishItems  =  list()

    #get the product
    product = Product.objects.get(pid=pid)

    #get the current logged user
    LoggedUser = User.objects.get(username=request.user)    
    
    #Check If item to add is already in WishList
    wishItemExist   =  WhishList.objects.all().filter(user=LoggedUser,product=product).exists()
    if not wishItemExist : 
            wish = WhishList.objects.create(user=LoggedUser,product=product)
            wish.save()               
    wishItems = WhishList.objects.all().filter(user=LoggedUser)
    return HttpResponse(len(wishItems))

@login_required(login_url="UserAuthsAPP:Login")
def RemoveWishProduct(request,pid):
    #get the product
    product = Product.objects.get(pid=pid)

    #get the current logged user
    LoggedUser = User.objects.get(username=request.user)    

    #Check If item to add is already in cart
    wishItemExist = WhishList.objects.filter(user=LoggedUser,product=product).exists()
    
    #Delete wish
    if wishItemExist : 
            wish = WhishList.objects.get(user=LoggedUser,product=product)            
            wish.delete()
    wishItems = WhishList.objects.all().filter(user=LoggedUser)
    return HttpResponse(len(wishItems))

@login_required(login_url="UserAuthsAPP:Login")
def RemoveAllWishes(request):
    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)

        #Get all wishes for the current user
        wishItems = WhishList.objects.all().filter(user=LoggedUser)

        for wish in wishItems:
            wish.delete()

        return redirect("ShopAPP:WishList")
