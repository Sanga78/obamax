import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from store.utils import cartData, guestOrder
# from .models import Accesory, Cart, CartItem, Order, OrderItem, Product
from .models import Accesory, Category, Customer, Order, OrderItem, Product, ShippingAddress
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    context= {'products':products,'cartItems': cartItems}
    return render(request,"index.html",context)

def product_detail(request,product_id):
    data = cartData(request)
    cartItems = data['cartItems']
    product = get_object_or_404(Product,id=product_id)
    accesories = Accesory.objects.filter(product=product)
    context = {
        'product' : product,
        'accesories' : accesories,
        'cartItems' : cartItems
    }
    return render(request,"product_detail.html", context)

def about_page(request):
    return render(request,"about.html")

def contact_us(request):
    return render(request,"contact.html")

def category(request, name):
    data = cartData(request)
    cartItems = data['cartItems']
    # Grab the category from the url
    try:
        category = Category.objects.get(name=name)
        cat_products = Product.objects.filter(category=category)
        return  render(request, "category.html", {'cat_products':cat_products, 'category':category,'cartItems':cartItems})

    except:
        messages.warning(request, "That category doesn't exist")
        return render(request,"category.html")

#search functionality
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')

        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
                )
            return render(request, "search.html", {'products':products})        
    else:
        return HttpResponse("<h2>Method Not Allowed</h2>")
#cart views
# @login_required
# def add_to_cart(request,product_id):
#     product = get_object_or_404(Product,id=product_id)
#     cart, created = Cart.objects.get_or_create(user= request.user)
#     cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product)
#     if not created:
#         cart_item.quantity +=1 
#     cart_item.save()
#     return redirect('store:cart_detail')

# @login_required
# def cart_detail(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     total_price = sum(item.get_total_price() for item in cart_items)
#     return render(request,"cart_detail.html",{'cart_items':cart_items,'total_price':total_price})

# @login_required
# def checkout(request):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_items = CartItem.objects.filter(cart=cart)
#     total_price = sum(item.get_total_price() for item in cart_items)
#     if request.method == 'POST':
#         order = Order.objects.create(user=request.user,total_price=total_price)
#         for item in cart_items:
#             OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity)
#         cart_items.delete()
#         return redirect('order_detail',order_id=order.id)     
#     return render(request,"check.html",{'cart_items':cart_items,'total_price':total_price})



def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context= {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'cart.html',context)

def checkout(request): 
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context= {'items':items, 'order':order,'cartItems':cartItems,'shipping':False}
    return render(request,'checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId:',productId)
    print('Action:',action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping ==True:
        ShippingAddress.objects.create(
            order = order,
            customer = customer,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse("Payment complete",safe=False)

#AUTHENTICATION VIEWS
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request,f"Logged in Successfully as {username}")
                customer, created = Customer.objects.get_or_create(user=request.user)
                return redirect('store:home_page')
            else:
                messages.info(request,"Account doesn't exists")
                return redirect('register')
        else:
            messages.info(request,'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
    
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                 # Logging in user
                user = authenticate(username=username, password=password)
                customer, created = Customer.objects.get_or_create(user=user)
                login(request, user)

            messages.success(request, "Registration successful")
            return redirect('store:home_page')
        else:
            messages.info(request,'Password Not The Same')
            return redirect('register')
    else:
        return render(request,'register.html')

def logout_request(request):
    logout(request)
    messages.info(request,"Logged out successfully!")
    return redirect('/')

@login_required
def profile(request):
    customer = get_object_or_404(Customer, user=request.user)
    orders = Order.objects.filter(customer=customer, complete=True)
    return render(request, 'profile.html', {'customer': customer, 'orders': orders})