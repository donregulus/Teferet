from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
# Create your models here.



STATUS_CHOICE = (
    ("process","Process"),
    ("shipped","Shipped"),
    ("delivered",'Delivered'),    
)

STATUS = ( 
    ("draft",'Draft'),
    ("disabled",'Disabled'),
    ("rejected",'Rejected'),
    ("inReview",'In Review'),    
    ("inReview",'In Review'),    
    ("Published",'Published'),    
)


RATINGS = (
    (1,'★☆☆☆☆'),    
    (2,'★★☆☆☆'),    
    (3,'★★★☆☆'),    
    (4,'★★★★☆'),    
    (5,'★★★★★'),        
)


class Category(models.Model):
    cid         = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=150,unique=True)
    image       = models.ImageField(upload_to="Categories",default="Category.jpg")
    description = models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self) -> str:
        return self.name


class Tags(models.Model):
    pass


class Product(models.Model):
    Category    = models.ForeignKey(Category, on_delete=models.CASCADE,null=False)
    tags        = models.ForeignKey(Tags, on_delete=models.SET_NULL,null=True)
    
    pid         = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=150)
    image       = models.ImageField(upload_to="Products",default="product.jpg")    
    description = models.TextField(null=False,blank=False)
    stock       = models.IntegerField(default=0)
    isAvailable = models.BooleanField(default=True)    
    price       = models.DecimalField(max_digits=99999,decimal_places=2)
    old_price   = models.DecimalField(max_digits=99999,decimal_places=2)    
    createdDate = models.DateTimeField(auto_now_add=True )
    updatedDate = models.DateTimeField(auto_now=True)    

    # product_status = models.CharField(choices=STATUS, max_length=10, default="inReview")
    # status = models.BooleanField(default=True)
    # in_Stock = models.BooleanField(default=True)
    # featured = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name    

    def getPercentage(self):
        return ((self.price/self.old_price)*100)

class ProductReview(models.Model):
    user        = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    review      = models.TextField()
    rating      = models.IntegerField(choices=RATINGS,default=None)
    createdDate = models.DateTimeField(auto_now_add=True )
    updatedDate = models.DateTimeField(auto_now=True)    

    def __str__(self) -> str:
        return self.product.name    
    
    def getRating(self):
        return self.rating

class WhishList(models.Model):
    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)  
    createdDate = models.DateTimeField(auto_now_add=True )

    def __str__(self) -> str:
        return self.product.name    