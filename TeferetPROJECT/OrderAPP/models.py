from django.db import models
from django.contrib.auth.models import User
from ShopAPP.models import Cart
import uuid

# Create your models here.

ORDERSTATUS = (
    (1,'IN PREPARATION'),    
    (2,'IN DELIVERY'),    
    (3,'RECEIVED')        
)

class Order(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    cart            = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    createdDate     = models.DateTimeField(auto_now_add=True )
    PaymentMode     = models.CharField(max_length=150)
    PaymentStatus   = models.CharField(max_length=150)    
    DeliveredStatus = models.IntegerField(choices=ORDERSTATUS,default=1,null=False)     
    userIpAddress   = models.CharField(max_length=150)
    providerOrderId = models.CharField(max_length=150)   
    totalAmout      = models.DecimalField(max_digits=99999,decimal_places=2, default=0.0)

    
