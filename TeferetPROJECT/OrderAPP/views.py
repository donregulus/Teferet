from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

# Create your views here.


from UserAuthsAPP.models import UserProfile

def PlaceOrder(request):
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                }       
        return render(request, 'OrderAPP/PlaceOrder.html',context)
    else:
        return render(request, 'OrderAPP/PlaceOrder.html')


@login_required(login_url="UserAuthsAPP:Login")
def PaypalPayment(request):
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                } 
        return render(request, 'OrderAPP/PaypalPayment.html',context)
    else:
        return render(request, 'OrderAPP/PaypalPayment.html')


@login_required(login_url="UserAuthsAPP:Login")
def CreditCardPayment(request):
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                } 
        return render(request, 'OrderAPP/CreditCardPayment.html',context)
    else:
        return render(request, 'OrderAPP/CreditCardPayment.html')