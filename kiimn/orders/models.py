from django.db import models
from shop.models import Product

class Order(models.Model):
    first_name = models.CharField(verbose_name='First Name', max_length=50)
    last_name = models.CharField(verbose_name='Last Name', max_length=50)
    address =  models.CharField(verbose_name='Address', max_length=250)
    postal_code = models.CharField(verbose_name='Postal Code', max_length=20)
    city = models.CharField(verbose_name='City', max_length=100)
    province = models.CharField(verbose_name='Province', max_length = 100)
    phone = models.CharField(verbose_name='Phone Number', max_length = 15)
    email = models.EmailField(verbose_name='Email')
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)
    paid = models.BooleanField(verbose_name='Paid', default=False)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=5)
    color = models.CharField(max_length = 200, verbose_name = "Color")
    size = models.CharField(max_length = 200, verbose_name = "Size")

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price
