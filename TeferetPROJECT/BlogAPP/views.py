from django.shortcuts import render

# Create your views here.

def blog(request):
    return render(request, "BlogAPP/Blog.html")



def blogDetails(request):
    return render(request, "BlogAPP/BlogDetails.html")