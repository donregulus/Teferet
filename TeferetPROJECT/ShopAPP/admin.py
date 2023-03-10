from django.contrib import admin
from .models import Category, WhishList,Product,ProductReview
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name","image","description"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name","image","price","description","createdDate","isAvailable"]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user","product","review","rating","createdDate"]

class WishListAdmin(admin.ModelAdmin):
    list_display = ["user","product","createdDate"]


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(WhishList,WishListAdmin)

