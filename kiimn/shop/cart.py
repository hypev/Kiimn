from django.conf import settings
from shop.models import Product
from decimal import Decimal

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, color, size):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price),
                                     'color': color,
                                     'size': size}
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
      product_id = str(product.id)
      if product_id in self.cart:
          del self.cart[product_id]
          self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        return len(self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
