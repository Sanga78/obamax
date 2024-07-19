from django.shortcuts import get_object_or_404, render
from .models import Product

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request,"store/product_list.html")

def product_detail(request,product_id):
    product = get_object_or_404(Product,id=product_id)