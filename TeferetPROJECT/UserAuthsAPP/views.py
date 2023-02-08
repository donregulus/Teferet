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


from UserAuthsAPP.forms import RegisterForm,LoginForm
from UserAuthsAPP.models import UserProfile

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
                return render(request,'UserAuthsAPP/Sign-up.html',context)   
                
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
            return render(request,'UserAuthsAPP/Sign-up.html',context)   
                
    else :         
        print("---------------Can not registered user")
        form = RegisterForm(request.POST or None)
        loginForm = LoginForm(data= None)
        context = {
                    'form' : form,
                    'loginForm' : loginForm,
                    'signUpView' : True
        }
        return render(request,'UserAuthsAPP/Sign-up.html',context)

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
            
            #Authentificate user and redirect to profile page            
            LoggedUser = auth.authenticate(username=userCreatedName,password=userCreatedPassword) 
            if LoggedUser is not None:
                auth.login(request,LoggedUser)   
                LoggedUser = User.objects.get(username=userCreatedName)
                LoggedUserProfile = UserProfile.objects.get(user=LoggedUser)
                context = {
                    "userProfile": LoggedUserProfile,
                }
                messages.success(request,"Logged in succefully !")  
                return render(request,"CoreAPP/Index.html",context)
            else:
                messages.error(request,"Credential Failed: Enter a correct username and password")    
                return render(request,'UserAuthsAPP/Sign-up.html',context)
        else:                      
            messages.error(request,"Credential Failed: Enter a correct username and password")                
            return render(request,'UserAuthsAPP/Sign-up.html',context)   
    else:    
        form      = RegisterForm(data=None)        
        loginForm = LoginForm(data= request.POST or None)
        context = {
                        'form' : form,
                        'loginForm' : loginForm,
                        
            }
        return render(request,'UserAuthsAPP/Sign-up.html',context)

@login_required(login_url="UserAuthsAPP:Login")
def Logout(request):        
    auth.logout(request)
    messages.success(request,"Logged out succefully !")  
    return redirect("UserAuthsAPP:Login")

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
                        LoggedUserProfile = UserProfile.objects.get(user=request.user)
                        context = {
                            "userProfile": LoggedUserProfile,
                            }   
                        return redirect("UserAuthsAPP:DashBoard")
                    else:                        
                        messages.error(request, "Failed to login after changing the password")
                        return redirect("CoreAPP:Index")
                else:
                    messages.error(request, 'New Password must be different from the current Password')
                    LoggedUserProfile = UserProfile.objects.get(user=request.user)
                    context = {
                            "userProfile": LoggedUserProfile,
                        }   
                    return render(request, "UserAuthsAPP/ChangePassword.html",context)   

            else:
                messages.error(request, 'Password do not match!')
                LoggedUserProfile = UserProfile.objects.get(user=request.user)
                context = {
                        "userProfile": LoggedUserProfile,
                    }   
                return render(request, "UserAuthsAPP/ChangePassword.html",context)   
        else:    
            print("request not post")
            LoggedUserProfile = UserProfile.objects.get(user=request.user)
            context = {
                        "userProfile": LoggedUserProfile,
                    }   
            return render(request, "UserAuthsAPP/ChangePassword.html",context)
 


@login_required(login_url="UserAuthsAPP:Login")
def DashBoard(request):    
    LoggedUserProfile = UserProfile.objects.get(user=request.user)
    context = {
                    "userProfile": LoggedUserProfile,
                }
    return render(request,"UserAuthsAPP/DashBoard.html",context)