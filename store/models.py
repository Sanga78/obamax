from django.conf import settings
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

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
    flash_sale_start_time = models.DateTimeField(null=True, blank=True)
    flash_sale_end_time = models.DateTimeField(null=True, blank=True)
    discount_percentage = models.FloatField(default=0)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model_number = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + str(uuid.uuid4()).replace('-','')[:5]
        super().save(*args, **kwargs)
    @property
    def get_average_rating(self):
        avg = self.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg']
        return avg if avg else 0
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
        if self.flash_sale_price and self.flash_sale_end_time and self.flash_sale_end_time > timezone.now():
            return self.flash_sale_price
        return self.price

    @property
    def get_discount_price(self):
        if self.discount_percentage > 0:
            return self.price * Decimal(1 - self.discount_percentage / 100)
        return self.price
    @property
    def get_flash_sale_countdown(self):
        if self.flash_sale_price and self.flash_sale_end_time and self.flash_sale_end_time > timezone.now():
            time_remaining = self.flash_sale_end_time - timezone.now()
            hours, remainder = divmod(time_remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return None
    @property
    def reviews_count(self):
        return self.reviews.count()
    def get_rating_count_for_star(self, star_value):
        return self.reviews.filter(rating=star_value).count()
    def get_review_count(self):
        return self.reviews.filter(is_approved=True).count()

    def get_rating_percentage(self, rating):
        total = self.reviews.filter(is_approved=True).count()
        if total == 0:
            return 0
        count = self.reviews.filter(is_approved=True, rating=rating).count()
        return (count / total) * 100

class ProductReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES,
                                            validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)  # For moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_purchase = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return f"{self.get_rating_display()} review for {self.product.name} by {self.user.username}"

class Accesory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='accessories')
    accessory_type = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='accessories/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.accessory_type} for {self.product.name}"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

#HANDLING UNREGISTERED USERS    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True,blank=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length= 200,null=True)
    email = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}" if self.user else self.name

    def __str__(self):
        return self.name
    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete= models.SET_NULL,null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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
        subtotal = sum([item.get_total for item in orderitems])
        return subtotal + self.shipping_cost + self.tax
    
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
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.price_at_purchase and self.product:
            self.price_at_purchase = self.product.price
        super().save(*args, **kwargs)
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