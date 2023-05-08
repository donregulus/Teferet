from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from random import shuffle


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
    Comments =  Comment.objects.all().filter(blog=blog.bid)
    commentNumber = len(Comments)

    CommentsList = list()
    for Com in Comments:               
        UserLoggedProfile = UserProfile.objects.get(user=Com.user)             
        CommentsList.append({"User":UserLoggedProfile,"CommentText":Com.commentText,"CommentDate":Com.createdDate})
    shuffle(CommentsList)

    tags = "Tags:   "
    for tag in blog.tags.values_list():
            tags += tag[1] + '  '
    context = {                   
                    "blog": blog,      
                    "commentNumber" : commentNumber,
                    "tags":tags,
                    "comments":CommentsList[:5]
            }   
    return render(request, "BlogAPP/BlogDetails.html",context)
    

@login_required(login_url="UserAuthsAPP:Login")
def SendComment(request):
     if request.method == 'POST':        
        blogId = request.POST['BlogId']
        blog = Blog.objects.get(bid=blogId)
        text = request.POST['Comment']
        LoggedUser = User.objects.get(username=request.user)    
        comment = Comment.objects.create(user=LoggedUser,blog=blog,commentText=text)
        comment.save()
        return redirect("BlogAPP:BlogDetails",bid=blogId)