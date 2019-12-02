from django.shortcuts import render, get_object_or_404, redirect
from .models import Brand, Category, Product, ProductImage
from django.urls import resolve
from django.core.paginator import Paginator
from .cart import Cart

def LandingPage(request):
    return render(request, 'shop/index.html', {
        'product': Product.objects.order_by('-id')[0],
        'categories': Category.objects.order_by('-id')[0:3],
        'products': Product.objects.order_by('-id')[0:10],
        'bottom_brands': Brand.objects.order_by('-id')[0:6],
        'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
        'brands': Brand.objects.order_by('-name')[0:8],
        'cart': Cart(request),
        'cart_len': len(Cart(request))
    })

def ProductList(request, slug=None):
    category = None
    brand = None
    products = Product.objects.filter(available=True)
    if slug:
        if resolve(request.path_info).url_name is "ProductListByCategory":
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)
        elif resolve(request.path_info).url_name is "ProductListByBrand":
            brand = get_object_or_404(Brand, slug=slug)
            products = products.filter(brand=brand)
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    product_list = paginator.get_page(page)
    next_page = product_list.next_page_number() if product_list.has_next() else page
    prev_page = product_list.previous_page_number() if product_list.has_previous() else page
    return render(request, 'shop/product/shop.html', {
        'category': category,
        'brand': brand,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'products': product_list.object_list,
        'count': paginator.count,
        'pages_count': paginator.num_pages,
        'page': product_list.number,
        'has_other': product_list.has_other_pages(),
        'has_next': product_list.has_next(),
        'has_prev': product_list.has_previous(),
        'next_page': next_page,
        'prev_page': prev_page,
        'all_w': Category.objects.filter(gender='Women').order_by('-name'),
        'all_m': Category.objects.filter(gender='Men').order_by('-name'),
        'all_b': Brand.objects.order_by('-name'),
        'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
        'brands': Brand.objects.order_by('-name')[0:8],
        'cart': Cart(request),
        'cart_len': len(Cart(request))
    })

def Search(request):
    products = []
    for p in Product.objects.filter(available=True):
        if request.POST.get('search') in p.name or request.POST.get('search') in p.category.name or request.POST.get('search') in p.brand.name:
            products.append(p)
    return render(request, 'shop/product/shop.html', {
        'keyword': request.POST.get('search'),
        'products': Paginator(products, 9).get_page(request.GET.get('page')).object_list,
        'count': Paginator(products, 9).count,
        'pages_count': Paginator(products, 9).num_pages,
        'page': Paginator(products, 9).get_page(request.GET.get('page')).number,
        'has_other': Paginator(products, 9).get_page(request.GET.get('page')).has_other_pages(),
        'has_next': Paginator(products, 9).get_page(request.GET.get('page')).has_next(),
        'has_prev': Paginator(products, 9).get_page(request.GET.get('page')).has_previous(),
        'next_page': Paginator(products, 9).get_page(request.GET.get('page')).next_page_number()
                    if Paginator(products, 9).get_page(request.GET.get('page')).has_next()
                    else request.GET.get('page'),
        'prev_page': Paginator(products, 9).get_page(request.GET.get('page')).previous_page_number()
                    if Paginator(products, 9).get_page(request.GET.get('page')).has_previous()
                    else request.GET.get('page'),
        'all_w': Category.objects.filter(gender='Women').order_by('-name'),
        'all_m': Category.objects.filter(gender='Men').order_by('-name'),
        'all_b': Brand.objects.order_by('-name'),
        'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
        'brands': Brand.objects.order_by('-name')[0:8],
        'cart': Cart(request),
        'cart_len': len(Cart(request))
    })

def ProductDetail(request, id, slug):
    return render(request, 'shop/product/detail.html', {
        'product': get_object_or_404(Product, id=id, slug=slug, available=True),
        'sizes': get_object_or_404(Product, id=id, slug=slug, available=True).sizes.split(", "),
        'colors': get_object_or_404(Product, id=id, slug=slug, available=True).colors.split(", "),
        'images': ProductImage.objects.filter(product__id__contains=get_object_or_404(Product, id=id, slug=slug, available=True).id).order_by('-id'),
        'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
        'brands': Brand.objects.order_by('-id')[0:8],
        'cart': Cart(request),
        'cart_len': len(Cart(request))
    })

def Contact(request):
    return render(request, 'shop/contact.html', {
        'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
        'brands': Brand.objects.order_by('-id')[0:8],
        'cart': Cart(request),
        'cart_len': len(Cart(request))
    })

def CartAdd(request, product_id, color="Specify", size="Specify"):
    Cart(request).add(product=get_object_or_404(Product, id=product_id), color=color, size=size)
    return redirect(request.META.get('HTTP_REFERER'))

def CartRemove(request, product_id):
    Cart(request).remove(product = get_object_or_404(Product, id=product_id))
    return redirect(request.META.get('HTTP_REFERER'))
