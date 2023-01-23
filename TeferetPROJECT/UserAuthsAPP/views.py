from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect


from UserAuthsAPP.forms import RegisterForm
from UserAuthsAPP.models import UserProfile

# Create your views here.

def Register(request):
    
    if request.method == "POST":        
        form = RegisterForm(data= request.POST or None)
        
        if form.is_valid():
            UserEmail = request.POST["email"]
            if User.objects.filter(email=UserEmail).exists():                
                context = {
                    'form' : form,
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
                    'signUpView' : True
            }
            messages.error(request,form.errors)
            return render(request,'UserAuthsAPP/sign-up.html',context)   
                
    else :         
        print("---------------Can not registered user")
        form = RegisterForm(request.POST or None)
        context = {
                    'form' : form,
                    'signUpView' : True
        }
        return render(request,'UserAuthsAPP/sign-up.html',context)