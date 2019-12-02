from django.db import models
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(max_length = 200, db_index = True, verbose_name = "Name")
    slug = models.SlugField(max_length = 200, db_index = True)
    image = models.ImageField(upload_to = 'brands/', blank = True, verbose_name = "Logo")

    class Meta:
        ordering = ['name']
        index_together = [
            ['name', 'slug']
        ]
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 200, db_index = True, verbose_name = "Name")
    gender = models.CharField(max_length = 200, db_index = True, verbose_name = "Gender")
    image = models.ImageField(upload_to = 'categories/', blank = True, verbose_name = "Template Image")
    slug = models.SlugField(max_length = 200, db_index = True)

    class Meta:
        ordering = ['name']
        index_together = [
            ['gender', 'slug']
        ]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return "[ " + self.gender[0] + " ] " + self.name

def product_image_path_preview(instance, filename):
    return "products/preview/{0}/{1}".format(instance.id, filename)

def product_image_path_hover(instance, filename):
    return "products/hover/{0}/{1}".format(instance.id, filename)

class Product(models.Model):
    brand = models.ForeignKey(Brand, related_name = 'brands', verbose_name = "Brand", on_delete = models.PROTECT)
    category = models.ForeignKey(Category, related_name = 'categories', verbose_name = "Category", on_delete = models.PROTECT)
    name = models.CharField(max_length = 200, db_index = True, verbose_name = "Name")
    slug = models.SlugField(max_length = 200, db_index = True)
    description = models.TextField(blank = True, verbose_name = "Description")
    colors = models.CharField(max_length = 200, verbose_name = "Colors")
    sizes = models.CharField(max_length = 200, verbose_name = "Sizes")
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Price")
    stock = models.PositiveIntegerField(verbose_name = "In stock")
    available = models.BooleanField(default = True, verbose_name = "Available")
    image_preview = models.ImageField(upload_to = product_image_path_preview, blank = True, verbose_name = "Product Preview")
    image_hover = models.ImageField(upload_to = product_image_path_hover, blank = True, verbose_name = "On Hover Preview")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return self.name

def image_path(instance, filename):
    return "products/{0}/{1}".format(instance.product.id, filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name = 'product', verbose_name = "Product", on_delete = models.PROTECT)
    image = models.ImageField(upload_to = image_path, blank = True, verbose_name = "Image")
    uploaded = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['updated']
        index_together = [
            ['id', 'image']
        ]

    def __str__(self):
        return self.product.name + "_image"
