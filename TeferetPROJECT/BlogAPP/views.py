from django.shortcuts import render
from django.contrib.auth.decorators import login_required 





from UserAuthsAPP.models import UserProfile

# Create your views here.

def Blog(request):   
    return render(request, "BlogAPP/Blog.html")


def BlogDetails(request):
    return render(request, "BlogAPP/BlogDetails.html")
    

@login_required(login_url="UserAuthsAPP:Login")
def SendComment(request):
    pass