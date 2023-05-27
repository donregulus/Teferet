from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder



from UserAuthsAPP.models import UserProfile
from ShopAPP.models import Product, Category, Cart, CartItem, WhishList
# Create your views here.


from django.core import serializers
import json
import uuid


from django.http import HttpResponse,JsonResponse


def __cart_id__(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()        
    # return uuid.UUID(str(cart)).hex
    return uuid.uuid1()

def __isAjax__(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return True
    else:
        return False

def ModalProductDetails(request,pid):
        
    quantity = 0
    product = Product.objects.get(pid=pid)
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
        if Cart.objects.filter(isActive=True,cartid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,cartid=__cart_id__(request))            
            #Check If item to add is already in cart
            cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
            if cartItemExist:
                quantity = CartItem.objects.get(cart=cart,product=product).quantity        
    
    context = {                    
                    "product" : product,
                    "quantity": quantity,
                }         
    return render(request, 'ShopAPP/ModalProductDetails.html',context)

def ProductDetails(request,pid):   

    quantity = 0
    product = Product.objects.get(pid=pid)
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
        if Cart.objects.filter(isActive=True,cartid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,cartid=__cart_id__(request))            
            #Check If item to add is already in cart
            cartItemExist = CartItem.objects.filter(cart=cart,product=product).exists()
            if cartItemExist:
                quantity = CartItem.objects.get(cart=cart,product=product).quantity        
    
    context = {                    
                    "product" : product,
                    "quantity": quantity,
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
        if Cart.objects.filter(isActive=True,cartid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,cartid=__cart_id__(request))
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
        if Cart.objects.filter(isActive=True,cartid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,cartid=__cart_id__(request))
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
        if Cart.objects.filter(isActive=True,cartid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,cartid=__cart_id__(request))
        else:         
            cart = Cart.objects.create(cartid=__cart_id__(request))
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
        if Cart.objects.filter(isActive=True,cartid=__cart_id__(request)).exists() :
            cart = Cart.objects.get(isActive=True,cartid=__cart_id__(request))
        else:         
            cart = Cart.objects.create(cartid=__cart_id__(request))
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
            item.delete()
            cart_items = CartItem.objects.all().filter(cart=cart)       
    
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

    