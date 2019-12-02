from django.shortcuts import render, get_object_or_404, redirect
from .models import Brand, Category, Product, ProductImage
from django.urls import resolve
from django.core.paginator import Paginator
from .cart import Cart

def LandingPage(request):
    bottom_brands = Brand.objects.order_by('-id')[0:6]
    product = Product.objects.order_by('-id')[0]
    categories = Category.objects.order_by('-id')[0:3]
    products = Product.objects.order_by('-id')[0:10]

    women_categories = Category.objects.filter(gender='Women').order_by('-name')[0:8]
    men_categories = Category.objects.filter(gender='Men').order_by('-name')[0:8]
    brands = Brand.objects.order_by('-name')[0:8]
    cart = Cart(request)
    cart_len = len(cart)
    return render(request, 'shop/index.html', {
        'product': product,
        'categories': categories,
        'products': products,
        'bottom_brands': bottom_brands,
        'w_categories': women_categories,
        'm_categories': men_categories,
        'brands': brands,
        'cart': cart,
        'cart_len': cart_len
    })

def ProductList(request, sort="newest", slug=None,):
    category = None
    brand = None
    categories = None
    products = None
    brands = None
    products = Product.objects.filter(available=True)
    cart = Cart(request)
    cart_len = len(cart)
    if slug:
        if resolve(request.path_info).url_name is "ProductListByCategory":
            categories = Category.objects.all()
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)
        elif resolve(request.path_info).url_name is "ProductListByBrand":
            brands = Brand.objects.all()
            brand = get_object_or_404(Brand, slug=slug)
            products = products.filter(brand=brand)
    if sort is "newest":
        products = products.order_by('-updated')
    elif sort is "name":
        products = products.order_by('-name')
    elif sort is "increase":
        products = products.order_by('-price')
    elif sort is "decrease":
        products = products.order_by('price')
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    next_page = page
    prev_page = page
    if (products.has_next()):
        next_page = products.next_page_number()
    if (products.has_previous()):
        prev_page = products.previous_page_number()
    return render(request, 'shop/product/shop.html', {
        'category': category,
        'brand': brand,
        'categories': categories,
        'brands': brands,
        'products': products.object_list,
        'count': paginator.count,
        'pages_count': paginator.num_pages,
        'page': products.number,
        'has_other': products.has_other_pages(),
        'has_next': products.has_next(),
        'has_prev': products.has_previous(),
        'next_page': next_page,
        'prev_page': prev_page,
        'all_w': Category.objects.filter(gender='Women').order_by('-name'),
        'all_m': Category.objects.filter(gender='Men').order_by('-name'),
        'all_b': Brand.objects.order_by('-name'),
        'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
        'brands': Brand.objects.order_by('-name')[0:8],
        'cart': cart,
        'cart_len': cart_len
    })

def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    images = ProductImage.objects.filter(product__id__contains=product.id).order_by('-id')
    sizes = product.sizes.split(", ")
    colors = product.colors.split(", ")

    cart = Cart(request)
    cart_len = len(cart)
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'sizes': sizes,
                                                        'colors': colors,
                                                        'images': images,
                                                        'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
                                                        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
                                                        'brands': Brand.objects.order_by('-id')[0:8],
                                                        'cart': cart,
                                                        'cart_len': cart_len})

def CartAdd(request, product_id, color = "Specify", size = "Specify"):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, color=color, size=size)
    return redirect(request.META.get('HTTP_REFERER'))

def CartRemove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect(request.META.get('HTTP_REFERER'))
