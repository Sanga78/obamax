from django.contrib import admin

from .models import Accesory, Category, Customer, Order, OrderItem, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Accesory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)