from django.shortcuts import render, get_object_or_404
from .models import Brand, Category, Product
from django.urls import resolve

def LandingPage(request):
    women_categories = Category.objects.filter(gender='Women').order_by('-id')[0:5]
    women_categories = Category.objects.filter(gender='Men').order_by('-id')[0:5]
    brands = Brand.objects.order_by('-id')[0:5]
    product = Product.objects.order_by('-id')[0]
    categories = Category.objects.order_by('-id')[0:3]
    products = Product.objects.order_by('-id')[0:10]
    return render(request, 'shop/index.html', {
        'product': product,
        'categories': categories,
        'products': products
    })

def ProductList(request, slug=None):
    category = None
    brand = None
    categories = None
    products = None
    brands = None
    products = Product.objects.filter(available=True)
    if slug:
        if resolve(request.path_info).url_name is "ProductListByCategory":
            categories = Category.objects.all()
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)
        elif resolve(request.path_info).url_name is "ProductListByBrand":
            brands = Brand.objects.all()
            brand = get_object_or_404(Brand, slug=slug)
            products = products.filter(category=category)
    return render(request, 'shop/product/shop.html', {
        'category': category,
        'brand': brand,
        'categories': categories,
        'brands': brands,
        'products': products
    })

def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    sizes = product.sizes.split(", ")
    colors = product.colors.split(", ")
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'sizes': sizes,
                                                        'colors': colors})
