from django.contrib import admin
from .models import Category, WhishList,Product,ProductReview,CartItem,Cart,ProductImages,Variation
# Register your models here.

class ProductImageAdmin(admin.TabularInline):
    model = ProductImages    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name","category_image","description"]

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ["name","product_image","price","description","createdDate","isAvailable"]


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user","product","review","rating","createdDate"]

class WishListAdmin(admin.ModelAdmin):
    list_display = ["user","product","createdDate"]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ["product","cart","quantity"]

class CartAdmin(admin.ModelAdmin):
    list_display = ["cartid","user","createdDate","isActive"]       


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value') 
  
    

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(WhishList,WishListAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Variation, VariationAdmin)

