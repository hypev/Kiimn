# KIIMN
We are team `Golden Trio+` and our project `Kiimn` - Django based brand clothing store.
## Team members
- [Kurbanali Ruslan](https://vk.com/hypev)
- [Aselya Kasymzhanova](https://vk.com/aselya116)
- [Temirlan Assanov](https://vk.com/rrrraaawww)
- [Serikkhan Ugylan](https://vk.com/thesugylan)
# The BIG Question: Why we dont have a login/registration?
  It's easy to explain. Because our Cart works with SESSION_ID which `key` is stores in our web-browser a long time ( default 5 weeks ).
  So, if person needs to buy a clothe's to this period of year, we think they dont need to be a registered to site, only fill the forms   devlivery purpose.
# Technical Part
## How works our website?
`Wrapper` of our site:
  1. filter by Gender - Category, Brand Name and Contact section. In the right side field to search Product and Cart.
  2. footer is only anchor links to route in the website and social media link's.
  3. About `Cart`: We can add Products only 1 example. Cupon System, if type a correct and actual code, site gives you discount. Pay attention that: OUR CART IS IN EVERY PAGE, SO WE SEND REQUIRED ELEMENTS IN EVERY 'views.py'. 
### In `Landing Page`:
  1. Section: Show Last Added Product Brand in to DataBase
  2. Section: Show Last Added 3 Categories in to Database and Special Cupon area with Code
  3. Section: Show Last Added 10 Product's in to Database
  4. Section: Show Last Added 6 Brand's in to Database
### In `Shop`:
  1. Also filter by Gender - Category and Brand name.
  2. We have a Pagination system ( max 9 products per page).
  3. The list with several information.
  4. Search result is on there.
### In `Product Detail`:
  1. List of Images.
  2. Detailed product information.
  3. Possibility add to Cart.
  4. We can choose the size and color, then add to cart
### In `Contact`:
  'nothing interesting :? scroll next
### In `Create Order`:
  Just collecting info from forms and inserting to DB.

## Dependence
1. `PIL` is the Python Imaging Library by Fredrik Lundh and Contributors.
```
pip install Pillow
```
2. `Django-PayPal` is the Payment System to Django Based Websites.
```
pip install django-paypal
```
## Installed App's
```
INSTALLED_APPS = [
    ...
    'paypal.standard.ipn',
    'shop',
    'orders',
    'payment',
    'cupons'
]
```
## Routing of files
```
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_URL = '/shop/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'shop/media/')
```
## Routing of Site
In the main `kiimn` directory `urls.py`:
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('order/', include(('orders.urls', 'orders'), namespace='orders')),
    path('paypal/', include(('paypal.standard.ipn.urls', 'paypal'), namespace='paypal')),
    path('payment/', include(('payment.urls', 'payment'), namespace='payment')),
    path('cupons/', include(('cupons.urls', 'cupons'), namespace='cupons'))
]
```
**In the `shop` app `urls.py`**:
```
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
```
**In the `orders` app `urls.py`**:
```
urlpatterns = [
    path('create/', views.OrderCreate, name='OrderCreate')
]
```
**In the `payment` app `urls.py`:**
```
urlpatterns = [
    path('process/', views.PaymentProcess, name='process'),
    path('done/', views.PaymentDone, name='done'),
    path('canceled/', views.PaymentCanceled, name='canceled')
]
```
**In the `cupons` app `urls.py`**:
```
urlpatterns = [
    path('apply', views.CuponApply, name='apply')
]
```
## Templating system
```
templates
  /orders
    create.html
  /payment
    done.html
    process.html
  /shop
    /product
      detail.html
      shop.html
     contact.html
     index.html
     wrapper.html
```
## Models
**`shop.models.Product`**
```
class Product(models.Model):
    brand = models.ForeignKey(Brand, related_name = 'brands', verbose_name = "Brand", on_delete = models.PROTECT)
    category = models.ForeignKey(Category, related_name = 'categories', verbose_name = "Category", on_delete = models.PROTECT)
    name = models.CharField(max_length = 50, db_index = True, verbose_name = "Name")
    slug = models.SlugField(max_length = 100, db_index = True)
    description = models.TextField(blank = True, verbose_name = "Description")
    colors = models.CharField(max_length = 200, verbose_name = "Colors(delim = ', ')")
    sizes = models.CharField(max_length = 200, verbose_name = "Sizes(delim = ', ')")
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Price($)")
    stock = models.PositiveIntegerField(verbose_name = "In stock")
    available = models.BooleanField(default = True, verbose_name = "Available")
    image_preview = models.ImageField(upload_to = product_image_path_preview, blank = True, verbose_name = "Product Preview")
    image_hover = models.ImageField(upload_to = product_image_path_hover, blank = True, verbose_name = "On Hover Preview")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
```
**`shop.models.ProductImage`**
```
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name = 'product', verbose_name = "Product", on_delete = models.PROTECT)
    image = models.ImageField(upload_to = image_path, blank = True, verbose_name = "Image")
    uploaded = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
```
**`shop.models.Category`**
```
class Category(models.Model):
    name = models.CharField(max_length = 20, db_index = True, verbose_name = "Name")
    gender = models.CharField(max_length = 10, db_index = True, verbose_name = "Gender")
    image = models.ImageField(upload_to = 'categories/', blank = True, verbose_name = "Template Image")
    slug = models.SlugField(max_length = 70, db_index = True)
```
**`shop.models.Brand`**
```
class Brand(models.Model):
    name = models.CharField(max_length = 20, db_index = True, verbose_name = "Name")
    slug = models.SlugField(max_length = 50, db_index = True)
    image = models.ImageField(upload_to = 'brands/', blank = True, verbose_name = "Logo")
```
**`orders.models.Order`**
```
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
    cupon = models.ForeignKey(Cupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(100)])
```
**`orders.models.OrderItem`**
```
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=5)
    color = models.CharField(max_length = 200, verbose_name = "Color")
    size = models.CharField(max_length = 200, verbose_name = "Size")
```
**`cupons.models.Cupon`**
```
class Cupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()
```
