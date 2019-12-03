from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from shop.cart import Cart
from shop.models import Category, Brand


def OrderCreate(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in Cart(request):
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         color=item['color'],
                                         size=item['size'])
            Cart(request).clear()
            return render(request, 'orders/order/created.html', {'order': order})

    form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
                                                        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
                                                        'brands': Brand.objects.order_by('-name')[0:8],
                                                        'cart': Cart(request),
                                                        'cart_len': len(Cart(request))})
