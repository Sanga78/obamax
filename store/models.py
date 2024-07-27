from django.conf import settings
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    digital = models.BooleanField(default=False, null=True, blank=False)
    flash_sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    flash_sale_end = models.DateTimeField(null=True, blank=True)
    discount_percentage = models.FloatField(default=0)

    def __str__(self):
        return self.name   

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 
    
    @property
    def get_flash_sale_price(self):
        if self.flash_sale_price and self.flash_sale_end and self.flash_sale_end > timezone.now():
            return self.flash_sale_price
        return self.price

    @property
    def get_discount_price(self):
        if self.discount_percentage > 0:
            return self.price * Decimal(1 - self.discount_percentage / 100)
        return self.price


class Accesory(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    accesory_type = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField()

    def __str__(self):
        return self.accesory_type


# METHOD 1

# class Cart(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def get_total_price(self):
#         return self.product.price * self.quantity
    
# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     total_price = models.DecimalField(max_digits=10,decimal_places=2)
#     is_paid = models.BooleanField(default=False)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()



#HANDLING UNREGISTERED USERS    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True,blank=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length= 200,null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete= models.SET_NULL,null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete= models.SET_NULL,null=True, blank=True)
    order = models.ForeignKey(Order,on_delete= models.SET_NULL,null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete= models.SET_NULL,null=True, blank=True)
    order = models.ForeignKey(Order,on_delete= models.SET_NULL,null=True, blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address