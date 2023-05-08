from django.contrib import admin
from .models import Blog , Tags , Comment
# Register your models here.

admin.site.register(Blog)
admin.site.register(Tags)
admin.site.register(Comment)

