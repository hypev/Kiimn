from django.contrib import admin
from .models import Order, OrderItem
from django.shortcuts import render, redirect, reverse
from .models import OrderItem
from .forms import OrderCreateForm
from shop.cart import Cart
from shop.models import Category, Brand
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_field = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'address', 'postal_code',
                    'city', 'province', 'phone', 'email', 'created', 'updated', 'paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
