from django.contrib import admin
from .models import Brand, Category, Product

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'slug']
    prepopulated_fields = {'slug': ('gender', 'name', )}

class ProductAdmin(admin.ModelAdmin):
    list_display = ['brand', 'category', 'name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available',]
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
