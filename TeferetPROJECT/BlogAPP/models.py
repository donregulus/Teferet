from django.db import models
from django.contrib.auth.models import User
import uuid



class Tags(models.Model):
    tid         = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title       = models.CharField(max_length=150,unique=True)
    createdDate = models.DateTimeField(auto_now_add=True )

    def __str__(self) -> str:
        return self.title


class Blog(models.Model):
    bid             = models.UUIDField(primary_key=True, default=uuid.uuid4)
    createdDate     = models.DateTimeField(auto_now_add=True )
    title           = models.CharField(max_length=150)
    image           = models.ImageField(upload_to="Blogs",default="blog.jpg")    
    fullDescription = models.TextField(null=False,blank=False)            
    summary         = models.TextField(null=False,blank=False)     
    tags            = models.ManyToManyField(Tags)

    def __str__(self) -> str:
        return self.title
    
class Comment(models.Model):    
    cid         = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    blog        = models.ForeignKey(Blog, on_delete=models.CASCADE, null=False)
    createdDate = models.DateField(auto_now_add=True)
    commentText = models.TextField(null=False,blank=False)                

    def __str__(self):
        return str(self.commentText)



    