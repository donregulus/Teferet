from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect


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
                return render(request,'UserAuthsAPP/sign-up.html',context)   
                
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
            return redirect("CoreAPP:index")

        else:
            context = {
                    'form' : form,
                    'loginForm' : loginForm,
                    'signUpView' : True
            }
            messages.error(request,form.errors)
            return render(request,'UserAuthsAPP/sign-up.html',context)   
                
    else :         
        print("---------------Can not registered user")
        form = RegisterForm(request.POST or None)
        loginForm = LoginForm(data= None)
        context = {
                    'form' : form,
                    'loginForm' : loginForm,
                    'signUpView' : True
        }
        return render(request,'UserAuthsAPP/sign-up.html',context)


def Login(request):

    print("login session")  

    if request.method == "POST":                
        print("request post")
        form      = RegisterForm(data=None)
        loginForm = LoginForm(data= request.POST or None)
        context = {
                        'form' : form,
                        'loginForm' : loginForm,
                        
            }
        if loginForm.is_valid():
            userCreatedName     = loginForm.cleaned_data.get("username")            
            userCreatedPassword = loginForm.cleaned_data.get("password")            
            
            #Authentificate user in and redirect to profile page            
            NewUserlogin = auth.authenticate(username=userCreatedName,password=userCreatedPassword) 
            if NewUserlogin is not None:
                auth.login(request,NewUserlogin)    
                return redirect("CoreAPP:index")
            else:
                messages.error(request,"Credential Failed: Enter a correct username and password")    
                return render(request,'UserAuthsAPP/sign-up.html',context)
        else:                      
            messages.error(request,"Credential Failed: Enter a correct username and password")    
            print(loginForm.errors)
            return render(request,'UserAuthsAPP/sign-up.html',context)   
    else:    
        form      = RegisterForm(data=None)        
        loginForm = LoginForm(data= request.POST or None)
        context = {
                        'form' : form,
                        'loginForm' : loginForm,
                        
            }
        return render(request,'UserAuthsAPP/sign-up.html',context)
