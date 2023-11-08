from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.html import mark_safe
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

COLORS = (
    (1,'⚫'),    
    (2,'🔴'),    
    (3,'🟢'),    
    (4,'🟡'),        
    (5,'🔵'),        
    (6,'⚪'),    
)



class Category(models.Model):
    cid         = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name        = models.CharField(max_length=150,unique=True)
    image       = models.ImageField(upload_to="Categories",default="Category.jpg")
    description = models.TextField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self) -> str:
        return self.name

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))


class Product(models.Model):
    Category    = models.ForeignKey(Category, on_delete=models.CASCADE,null=False)
    # tags        = models.ForeignKey(Tags, on_delete=models.SET_NULL,null=True)
    
    pid         = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name        = models.CharField(max_length=150)
    image       = models.ImageField(upload_to="Products",default="product.jpg")    
    description = models.TextField(null=False,blank=False)
    stock       = models.IntegerField(default=0)
    isAvailable = models.BooleanField(default=True)    
    price       = models.DecimalField(max_digits=99999,decimal_places=2)
    old_price   = models.DecimalField(max_digits=99999,decimal_places=2)    
    createdDate = models.DateTimeField(auto_now_add=True )
    updatedDate = models.DateTimeField(auto_now=True)    
    color       = models.IntegerField(choices=COLORS,default=1,null=True)

    # product_status = models.CharField(choices=STATUS, max_length=10, default="inReview")
    # status = models.BooleanField(default=True)
    # in_Stock = models.BooleanField(default=True)
    # featured = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name    

    def getPercentage(self):
        return ((self.price/self.old_price)*100)

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))


class ProductImages(models.Model):
    image   = models.ImageField(upload_to="ProductImages",default="product.jpg")    
    product = models.ForeignKey(Product,related_name="productAllImages", on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name_plural="Product Images"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))



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
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)  
    createdDate = models.DateTimeField(auto_now_add=True )

    def __str__(self) -> str:
        return self.product.name    
    

class Cart(models.Model):    
    cartid      =  models.UUIDField(primary_key=True, default=uuid.uuid4)
    user        =  models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdDate =  models.DateField(auto_now_add=True)
    isActive    =  models.BooleanField(default=True) 
    sessionid   =  models.CharField(max_length=250,null=True)      

    def __str__(self):
        return str(self.cartid)
    

class CartItem(models.Model):    
    cartItemid =  models.UUIDField(primary_key=True, default=uuid.uuid4) 
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)    
    cart       = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity   = models.IntegerField()
    variation  = models.CharField(max_length=100)

    def sub_total(self):
        return self.product.price * self.quantity


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category  = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=False)
    created_date        = models.DateTimeField(auto_now=True)
    quantity            = models.IntegerField(default=0)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
 