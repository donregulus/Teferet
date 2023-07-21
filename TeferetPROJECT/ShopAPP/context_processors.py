from django.contrib.auth.models import User

from .models import Cart, CartItem, WhishList
from .views  import __cart_id__


def counter(request):
    Itemscount = 0   
    WishCount = 0   

    if request.user.is_authenticated:
        #Get The current user
        LoggedUser = User.objects.get(username=request.user)    
        #Get the current cart
        cart = None
        if Cart.objects.filter(isActive=True,user=LoggedUser).exists() :
            cart = Cart.objects.get(isActive=True,user=LoggedUser)
        cart_items = CartItem.objects.all().filter(cart=cart)

        wishItems = WhishList.objects.all().filter(user=LoggedUser)
        WishCount = len(wishItems)
    else:
        #Get the current cart
        # request.session["logout"]= False   
        # request.session["login"]= False  
        cart = None
        sessionId= __cart_id__(request)
        if Cart.objects.filter(isActive=True,sessionid=sessionId,user=None).exists() :
            cart = Cart.objects.get(isActive=True,sessionid=sessionId,user=None)
            
        cart_items = CartItem.objects.all().filter(cart=cart)

    for cart_item in cart_items:
        Itemscount += cart_item.quantity    

    return dict(Itemscount=Itemscount, WishCount=WishCount)
