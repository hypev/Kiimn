from django.shortcuts import render, get_object_or_404
from decimal import *
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt
from shop.cart import Cart
from shop.models import Category, Brand, Product
from cupons.forms import CuponApplyForm


@csrf_exempt
def PaymentDone(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    order.paid = True
    order.save()
    return render(request, 'payment/done.html', {'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
                                                'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
                                                'brands': Brand.objects.order_by('-name')[0:8],
                                                'cart': Cart(request),
                                                'cart_len': len(Cart(request)),
                                                'cupon_apply_form': CuponApplyForm()})

@csrf_exempt
def PaymentCanceled(request):
    return render(request, 'payment/canceled.html', {'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
                                                    'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
                                                    'brands': Brand.objects.order_by('-name')[0:8],
                                                    'cart': Cart(request),
                                                    'cart_len': len(Cart(request)),
                                                    'cupon_apply_form': CuponApplyForm()})


def PaymentProcess(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost(),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled'))
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html',{'order':order, 'form':form,
                                                    'w_categories': Category.objects.filter(gender='Women').order_by('-name')[0:8],
                                                    'm_categories': Category.objects.filter(gender='Men').order_by('-name')[0:8],
                                                    'brands': Brand.objects.order_by('-name')[0:8],
                                                    'cart': Cart(request),
                                                    'cart_len': len(Cart(request)),
                                                    'cupon_apply_form': CuponApplyForm()})
