from django.db import models
from django.contrib.auth.models import User
from ShopAPP.models import Cart
import uuid

# Create your models here.

class Order(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    cart         = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    createdDate  = models.DateTimeField(auto_now_add=True )
    PaymentMode  = models.CharField(max_length=150)
    
