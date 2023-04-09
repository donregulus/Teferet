from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

from BlogAPP.models import Blog, Tags, Comment





from UserAuthsAPP.models import UserProfile

# Create your views here.

def Blogs(request):   

    blogs = Blog.objects.all()
    blogsInfo = list()
    for blog in blogs:        
        tags = "Tags:   "
        for tag in blog.tags.values_list():
            tags += tag[1] + '  '
        commentNumber = len(Comment.objects.all().filter(blog=blog.bid))
        blogInfo = {
            "tags":tags,
            "commentNumber":commentNumber,
            "blog":blog
        }
        blogsInfo.append(blogInfo)    
    context = {                   
                    "blogs": blogsInfo,                 
            }           
    return render(request, "BlogAPP/Blog.html",context)


def BlogDetails(request,bid):
    blog = Blog.objects.get(bid=bid)
    commentNumber = len(Comment.objects.all().filter(blog=blog.bid))
    tags = "Tags:   "
    for tag in blog.tags.values_list():
            tags += tag[1] + '  '
    context = {                   
                    "blog": blog,      
                    "commentNumber" : commentNumber,
                    "tags":tags
            }   
    return render(request, "BlogAPP/BlogDetails.html",context)
    

@login_required(login_url="UserAuthsAPP:Login")
def SendComment(request):
    pass