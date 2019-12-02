from django.contrib import admin
from .models import Brand, Category, Product, ProductImage

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'slug']
    prepopulated_fields = {'slug': ('name', )}
    list_editable = ['image']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'image', 'slug']
    prepopulated_fields = {'slug': ('gender', 'name', )}
    list_editable = ['image']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'category', 'name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available',]
    prepopulated_fields = {'slug': ('name', )}

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'updated']
    list_editable = ['image']

admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
