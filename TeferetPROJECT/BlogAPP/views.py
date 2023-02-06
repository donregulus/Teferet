from django.shortcuts import render
from django.contrib.auth.decorators import login_required 





from UserAuthsAPP.models import UserProfile

# Create your views here.

def Blog(request):
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                }       
        return render(request, "BlogAPP/Blog.html",context)
    else:
        return render(request, "BlogAPP/Blog.html")


def BlogDetails(request):
    if request.user.is_authenticated:        
        LoggedUserProfile = UserProfile.objects.get(user=request.user)
        context = {
                    "userProfile": LoggedUserProfile,
                }       
        return render(request, "BlogAPP/BlogDetails.html",context)
    else:
        return render(request, "BlogAPP/BlogDetails.html")
    

@login_required(login_url="UserAuthsAPP:Login")
def SendComment(request):
    pass