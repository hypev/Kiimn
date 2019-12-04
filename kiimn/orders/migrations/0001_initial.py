# Generated by Django 2.2.7 on 2019-12-03 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0003_auto_20191203_2131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('address', models.CharField(max_length=250, verbose_name='Address')),
                ('postal_code', models.CharField(max_length=20, verbose_name='Postal Code')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('province', models.CharField(max_length=100, verbose_name='Province')),
                ('phone', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=5, max_digits=10, verbose_name='Price')),
                ('colors', models.CharField(max_length=200, verbose_name='Color')),
                ('sizes', models.CharField(max_length=200, verbose_name='Size')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='orders.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='shop.Product')),
            ],
        ),
    ]