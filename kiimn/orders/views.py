from django.shortcuts import render, redirect, reverse
from .models import OrderItem
from .forms import OrderCreateForm
from shop.cart import Cart
from shop.models import Category, Brand
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from cupons.forms import CuponApplyForm

def OrderCreate(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            if Cart(request).cupon:
                order.cupon = Cart(request).cupon
                order.discount = Cart(request).cupon.discount
                order.save()
            for item in Cart(request):
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         color=item['color'],
                                         size=item['size'])
                product = item['product']
                product.stock -= 1
                if product.stock is 0:
                    product.available = False
                    product.save()
            Cart(request).clear()
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))

    form = OrderCreateForm()
    return render(request, 'orders/create.html', {'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
                                                        'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
                                                        'brands': Brand.objects.order_by('-name')[0:8],
                                                        'cart': Cart(request),
                                                        'cart_len': len(Cart(request)),
                                                        'cupon_apply_form': CuponApplyForm()})
