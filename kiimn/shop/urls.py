"""kiimn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from . import views

shop_patterns = [
    path('', views.ProductList, name='ProductList'),
    path('category/<slug:slug>/', views.ProductList, name='ProductListByCategory'),
    path('brand/<slug:slug>/', views.ProductList, name='ProductListByBrand'),
    path('<int:id>/<slug:slug>/', views.ProductDetail, name='ProductDetail')
]

cart_patterns = [
    path('add/<int:product_id>/', views.CartAdd, name='CartAdd'),
    path('remove/<int:product_id>/', views.CartRemove, name='CartRemove')
]

urlpatterns = [
    path('', views.LandingPage, name='LandingPage'),
    path('shop/', include(shop_patterns)),
    path('cart/', include(cart_patterns)),
    path('search/', views.Search, name='Search'),
    path('contact/', views.Contact, name='Contact')
]
