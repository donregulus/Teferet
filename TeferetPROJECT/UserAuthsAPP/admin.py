from django.contrib import admin
from . import models


# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    
     fieldsets = [
        ('Information',               {'fields': ['dateOfBirth','phoneNumber','bio']}),
        ('Location', {'fields': ['address','town','county','country','post_code','longitude','latitude']}),
    ]
admin.site.register(models.UserProfile,UserProfileAdmin)