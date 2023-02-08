from django.db import models
from django.contrib.auth.models import User

from datetime import datetime



# Create your models here.

class UserProfile(models.Model):
    """
    @class UserProfile
    This class extend the User model for auth
    """
    user          = models.OneToOneField(User, on_delete=models.CASCADE)        
    id            = models.AutoField(primary_key=True)    
    dateOfBirth   = models.DateField(default=datetime.now)
    phoneNumber   = models.CharField(verbose_name="Phone Number",max_length=150 ,null=True, blank=False)    
    profileImg    = models.ImageField(upload_to='profile_images', default="blank-profile-picture.png")


    address       = models.CharField(verbose_name="Address"  ,max_length=150 ,null=True, blank=True)
    town          = models.CharField(verbose_name="Town/City",max_length=150 ,null=True, blank=True)    
    country       = models.CharField(verbose_name="Country"  ,max_length=150 ,null=True, blank=True)
    post_code     = models.CharField(verbose_name="Post Code",max_length=8   ,null=True, blank=True)    

    """
    @fn __str__
    @private
    @Return Return User as string
    """
    def __str__(self):
        return f'{self.user}'
    