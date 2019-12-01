from django.db import models
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField(max_length = 200, db_index = True, verbose_name = "Name")
    slug = models.SlugField(max_length = 200, db_index = True)

    class Meta:
        ordering = ['name']
        index_together = [
            ['name', 'slug']
        ]
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:ProductList', args=[self.name, self.slug])

class Category(models.Model):
    name = models.CharField(max_length = 200, db_index = True, verbose_name = "Name")
    gender = models.CharField(max_length = 200, db_index = True, verbose_name = "Gender")
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

    def get_absolute_url(self):
        return reverse('shop:ProductList', args=[self.gender, self.slug])

class Product(models.Model):
    brand = models.ForeignKey(Brand, related_name = 'brands', verbose_name = "Brand", on_delete = models.PROTECT)
    category = models.ForeignKey(Category, related_name = 'categories', verbose_name = "Category", on_delete = models.PROTECT)
    name = models.CharField(max_length = 200, db_index = True, verbose_name = "Name")
    slug = models.SlugField(max_length = 200, db_index = True)
    image = models.ImageField(upload_to = 'products/%Y/%m/%d/', blank = True, verbose_name = "Image")
    description = models.TextField(blank = True, verbose_name = "Description")
    colors = models.CharField(max_length = 200, verbose_name = "Colors")
    sizes = models.CharField(max_length = 200, verbose_name = "Sizes")
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Price")
    stock = models.PositiveIntegerField(verbose_name = "In stock")
    available = models.BooleanField(default = True, verbose_name = "Available")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
          return reverse('shop:ProductDetail', args=[self.id, self.slug])
