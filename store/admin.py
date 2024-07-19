from django.contrib import admin

from .models import Accesory, Category, Product

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Accesory)