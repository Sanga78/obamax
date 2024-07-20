from django.shortcuts import get_object_or_404, render
from .models import Accesory, Product

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request,"index.html",{'products':products})

def product_detail(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    accesories = Accesory.objects.filter(product=product)
    context = {
        'product' : product,
        'accesories' : accesories
    }
    return render(request,"product_detail.html", context)