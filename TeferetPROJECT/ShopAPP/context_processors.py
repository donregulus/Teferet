from .models import Cart, CartItem
# from .views import _cart_id


def counter(request):
    Itemscount = 0

    #Get the current cart
    cart = None
    if Cart.objects.filter(isActive=True).exists() :
        cart = Cart.objects.get(isActive=True)
    else:         
        cart = Cart.objects.create()
        cart.save()    
   

    if request.user.is_authenticated:
            cart_items = CartItem.objects.all().filter(user=request.user)
    else:
        cart_items = CartItem.objects.all().filter(cart=cart)

    for cart_item in cart_items:
        Itemscount += cart_item.quantity

    return dict(Itemscount=Itemscount)
