from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 


# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage


from UserAuthsAPP.forms import RegisterForm,LoginForm,ProfileInfoForm
from UserAuthsAPP.models import UserProfile
from ShopAPP.models import  Cart, CartItem
from ShopAPP.views  import __cart_id__

# Create your views here.
def Register(request):
    
    if request.method == "POST":        
        form = RegisterForm(data= request.POST or None)
        loginForm = LoginForm(data= None)
        
        if form.is_valid():
            UserEmail = request.POST["email"]
            if User.objects.filter(email=UserEmail).exists():                
                context = {
                    'form' : form,
                    'loginForm' : loginForm,
                    'signUpView' : True
                }
                messages.error(request,"Email already used")
                return render(request,'UserAuthsAPP/SignUp.html',context)   
                
            form.save()            
            userCreatedName     = form.cleaned_data.get("username")            
            userCreatedPassword = form.cleaned_data.get("password1")            
            
            #log user in and redirect to profile page
            NewUserlogin = auth.authenticate(username=userCreatedName,password=userCreatedPassword)
            auth.login(request,NewUserlogin)

            #create profile for the new user
            NewUser     = User.objects.get(username=userCreatedName)
            NewUserProfile = UserProfile.objects.create(user=NewUser,id=NewUser.id)
            NewUserProfile.save()     
            messages.success(request,"Logged in succefully !")  
            return redirect("CoreAPP:Index")

        else:
            context = {
                    'form' : form,
                    'loginForm' : loginForm,
                    'signUpView' : True
            }
            messages.error(request,form.errors)
            return render(request,'UserAuthsAPP/SignUp.html',context)   
                
    else :         
        print("---------------Can not registered user")
        form = RegisterForm(request.POST or None)
        loginForm = LoginForm(data= None)
        context = {
                    'form' : form,
                    'loginForm' : loginForm,
                    'signUpView' : True
        }
        return render(request,'UserAuthsAPP/SignUp.html',context)

def Login(request):    

    if request.user.is_authenticated:
        return redirect("CoreAPP:Index")

    if request.method == "POST":                        
        form      = RegisterForm(data=None)
        loginForm = LoginForm(data= request.POST or None)
        context = {
                        'form' : form,
                        'loginForm' : loginForm,
                        
            }
        if loginForm.is_valid():
            userCreatedName     = loginForm.cleaned_data.get("username")            
            userCreatedPassword = loginForm.cleaned_data.get("password")            
            
            #Get previous session id
            AnonymousSessionId=__cart_id__(request)

            #Authentificate user and redirect to profile page            
            LoggedUser = auth.authenticate(username=userCreatedName,password=userCreatedPassword) 
            if LoggedUser is not None:
               
                cart = None
                if Cart.objects.filter(isActive=True,sessionid=AnonymousSessionId,user=None).exists():

                    #Get the current seession cart
                    cart = Cart.objects.get(isActive=True,sessionid=AnonymousSessionId,user=None)
                    cart_items = CartItem.objects.all().filter(cart=cart)

                    #Get The current user
                    LoggedUser = User.objects.get(username=userCreatedName)

                    #Get the current user cart
                    if Cart.objects.filter(isActive=True,user=LoggedUser).exists():
                        userCart = Cart.objects.get(isActive=True,user=LoggedUser)
                        userCart_items = CartItem.objects.all().filter(cart=userCart)
                        for item in cart_items:
                            for userItemLoop in userCart_items:
                                if item.product.pid == userItemLoop.product.pid:
                                    AnonymousProductId = item.product.pid
                                    AnonymousProductQuantity = item.quantity
                                    item.delete()
                                    userItem =  CartItem.objects.get(cart=userCart,product=AnonymousProductId)
                                    userItem.quantity +=AnonymousProductQuantity
                                    userItem.save()
                                    break
                                else:
                                    item.cart=userCart
                                    item.save()
                    else:         
                        Newcart = Cart.objects.create(user=LoggedUser,sessionid=__cart_id__(request))
                        Newcart.save()
                        for item in cart_items:                            
                            item.cart=Newcart
                            item.save()
                    cart.delete()                    

                auth.login(request,LoggedUser)                   
                messages.success(request,"Logged in succefully !")                
                return redirect("CoreAPP:Index")
            else:
                messages.error(request,"Credential Failed: Enter a correct username and password")    
                return render(request,'UserAuthsAPP/SignUp.html',context)
        else:                      
            messages.error(request,"Credential Failed: Enter a correct username and password")                
            return render(request,'UserAuthsAPP/SignUp.html',context)   
    else:    
        form      = RegisterForm(data=None)        
        loginForm = LoginForm(data= request.POST or None)
        context = {
                        'form' : form,
                        'loginForm' : loginForm,
                        
            }
        return render(request,'UserAuthsAPP/SignUp.html',context)

@login_required(login_url="UserAuthsAPP:Login")
def Logout(request):        
    auth.logout(request)       
    # request.session["logout"]= True   
    #     
    # request.session["login"]= False     
    messages.success(request,"Logged out succefully !")  
    return redirect("CoreAPP:Index")

def ForgotPassword(request):
    if request.method == 'POST':        
        UserEmail = request.POST['email']
        if User.objects.filter(email=UserEmail).exists():           
            user = User.objects.get(email__exact=UserEmail)      

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('UserAuthsAPP/EmailResetPassword.html', {
                'user': user,
                'domain': current_site,
                'site_name' : 'Teferet',
                'protocol' : 'https',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })                        
            UserEmail = "stroalgo@gmail.com"
            send_email = EmailMessage(mail_subject, message,from_email="noreply@Teferet.com", to=[UserEmail],)
            send_email.send()

            messages.success(request, 'An Email has been sent to your email address.')
            return redirect("UserAuthsAPP:Login")
        else:
            messages.error(request, 'Account does not exist!')
            return render(request, 'UserAuthsAPP/ForgotPassword.html')
    else:
        return render(request, 'UserAuthsAPP/ForgotPassword.html')

def EmailResetPassword(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid        
        return redirect('UserAuthsAPP:ResetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('UserAuthsAPP:Login')

def ResetPassword(request):   
    if request.method == 'POST':
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()            
            return redirect('UserAuthsAPP:Login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('UserAuthsAPP:ResetPassword')
    else:
        return render(request, 'UserAuthsAPP/ResetPassword.html')

@login_required(login_url="UserAuthsAPP:Login")
def ChangePassword(request):
        
        if request.method == 'POST':
        
            password = request.POST['password1']
            confirm_password = request.POST['password2']
            user = User.objects.get(username=request.user)                                   

            if password == confirm_password:    
                print("password 1 and 2 differ")                  
                if not (user.check_password(password)):
                    user.set_password(password)
                    user.save()
                    #Authentificate user and redirect to profile page            
                    LoggedUser = auth.authenticate(username=user.username,password=password)
                    if LoggedUser is not None:
                        auth.login(request,LoggedUser)            
                        messages.success(request, 'Password Changed Succefully !')                       
                        return redirect("UserAuthsAPP:DashBoard")
                    else:                        
                        messages.error(request, "Failed to login after changing the password")
                        return redirect("CoreAPP:Index")
                else:
                    messages.error(request, 'New Password must be different from the current Password')
                    LoggedUserProfile = UserProfile.objects.get(user=request.user)                      
                    return render(request, "UserAuthsAPP/ChangePassword.html")   

            else:
                messages.error(request, 'Password do not match!')
                LoggedUserProfile = UserProfile.objects.get(user=request.user)                   
                return render(request, "UserAuthsAPP/ChangePassword.html")   
        else:                           
            return render(request, "UserAuthsAPP/ChangePassword.html")

@login_required(login_url="UserAuthsAPP:Login")
def DashBoard(request):    
    return render(request,"UserAuthsAPP/DashBoard.html")

@login_required(login_url="UserAuthsAPP:Login")
def EditProfile(request):
    if request.method == 'POST':   
        userLogged            = User.objects.get(username=request.user)        
        userLogged.first_name = request.POST["first_name"]
        userLogged.last_name  = request.POST["last_name"]
        userLogged.username   = request.POST["username"]
        userLogged.email      = request.POST["email"]        
        userLogged.save()      
        messages.success(request, 'Your Personal Informations has been updated.')
        return redirect('UserAuthsAPP:DashBoard')  
    else:        
        Userform    = RegisterForm()            
        context = {
                        'form' : Userform,                        
            }
        return render(request,"UserAuthsAPP/EditProfile.html",context)

@login_required(login_url="UserAuthsAPP:Login")
def EditAddress(request):    
    if request.method == 'POST':
        UserLoggedProfile             = UserProfile.objects.get(user=request.user)        
        UserLoggedProfile.dateOfBirth = request.POST["dateOfBirth"]
        UserLoggedProfile.phoneNumber = request.POST["phoneNumber"]
        UserLoggedProfile.address     = request.POST["address"]
        UserLoggedProfile.town        = request.POST["town"]
        UserLoggedProfile.country     = request.POST["country"]
        UserLoggedProfile.post_code   = request.POST["post_code"]
        UserLoggedProfile.profileImg  = request.FILES.get('profileImg')
        UserLoggedProfile.save()
        messages.success(request, 'Your Profile Informations has been updated.')
        return redirect('UserAuthsAPP:ViewAddress')  
    else:
        ProfileForm = ProfileInfoForm()        
        context = {                        
                        'ProfileForm' : ProfileForm,                            
            }
    return render(request,"UserAuthsAPP/EditAddress.html",context)

@login_required(login_url="UserAuthsAPP:Login")
def ViewAddress(request):    
    return render(request,"UserAuthsAPP/ViewAddress.html")