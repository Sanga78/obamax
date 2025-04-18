import datetime
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from store.decorators import login_required_superadmin_required
from store.utils import cartData, guestOrder
from django.db.models import Sum,F
from .models import Accesory, Category, Customer, Order, OrderItem, Product, ShippingAddress,ProductReview
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, CustomerCreationForm, ProductForm, ReviewForm
from django.views.decorators.http import require_POST
from django.contrib import auth
# Create your views here.
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()
    flash_sales = Product.objects.filter(flash_sale_end_time__gt=timezone.now())
    for product in flash_sales:
        print(product.name)
    context = {'products': products, 'cartItems': cartItems, 'flash_sales': flash_sales}
    return render(request, "index.html", context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = cartData(request)
    cartItems = data['cartItems']
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    # Handle review submission
    review_form = None
    if request.user.is_authenticated:
        user_review = ProductReview.objects.filter(
            product=product, 
            user=request.user
        ).first()
        
        if request.method == 'POST' and 'submit_review' in request.POST:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Review submitted successfully!')
                return redirect('store:product_detail', product_id=product.id)
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = ReviewForm()
    
    # Get approved reviews
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    rating_percentages = {i: product.get_rating_percentage(i) for i in range(1, 6)}
    user_review = reviews.filter(user=request.user).first() if request.user.is_authenticated else None

    context = {
        'product': product,
        'cartItems':cartItems,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': ReviewForm(),
        'average_rating': product.get_average_rating, 
        'review_count': reviews.count(),
        'rating_percentages': rating_percentages,
        'user_has_reviewed': user_review is not None,
        'user_review_id': user_review.id if user_review else None,
    }

    return render(request, 'product_detail.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Your review has been deleted.')
    return redirect('product_detail', product_id=product_id)
def about_page(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request,"about.html",{'cartItems':cartItems})

def contact_us(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request,"contact.html",{'cartItems':cartItems})

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
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'GET':
        query = request.GET.get('query')

        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
                )
            return render(request, "search.html", {'products':products,'cartItems':cartItems})        
    else:
        return HttpResponse("<h2>Method Not Allowed</h2>")

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
    next = request.GET.get('next') or None
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                print("logged in Successfully")
                if user.is_superuser:
                    if next:
                        return redirect(next)
                    return redirect('store:admin_home') 
                else:
                    if next:
                        return redirect(next)
                    customer, created = Customer.objects.get_or_create(user=request.user)
                    return redirect('store:home_page')
            else:
                messages.info(request,"Account doesn't exists")
                return redirect('register')
        else:
            messages.info(request,'Invalid credentials')
    else:
        form = AuthenticationForm()
    context={'cartItems':cartItems}
    return render(request, 'login.html',context)

def register(request):
    data = cartData(request)
    cartItems = data['cartItems']
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
                customer, created = Customer.objects.get_or_create(user=user,name=username,email=email)
                login(request, user)

            messages.success(request, "Registration successful")
            return redirect('store:home_page')
        else:
            messages.info(request,'Password Not The Same')
            return redirect('register')
    else:
        context={'cartItems':cartItems}
        return render(request,'register.html',context)

@login_required
def profile(request):
    customer = get_object_or_404(Customer, user=request.user)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    orders = Order.objects.filter(customer=customer)
    print(orders)
    context ={'customer': customer, 'orders': orders,'cartItems':cartItems,'items':items}
    return render(request, 'profile.html',context)
@login_required
def update_profile(request):
    if request.method != "POST":
        HttpResponse("<h1>Method Not Allowed</h1>")
    else:
        name = request.POST["name"]
        email = request.POST["email"]
        phone_no = request.POST["phone"]

        customer = Customer.objects.get(user=request.user)
        customer.name = name
        customer.email = email
        customer.phone_no = phone_no
        customer.save()

    return HttpResponseRedirect("profile")


# ADMIN VIEWS
@login_required_superadmin_required
def admin_home(request):
    products = Product.objects.all().order_by('-id')[:10]
    customers = Customer.objects.all().order_by('-id')[:8]
    orders = Order.objects.filter(complete=True).order_by('-date_ordered')[:8]
    
    today = timezone.now().date()
    daily_sales = Order.objects.filter(
        date_ordered__date=today,
        complete=True
    ).count()
    
    total_orders = Order.objects.filter(complete=True).count()
    
    total_earnings = sum(order.get_cart_total for order in Order.objects.filter(complete=True))
    context = {
        "products": products,
        "customers": customers,
        "orders": orders,
        "daily_sales": daily_sales,
        "total_orders": total_orders,
        "total_earnings": f"{total_earnings:,.2f}",
        "total_reviews": 284, 
    }
    return render(request, "admin/home.html", context)
@login_required_superadmin_required
def admin_view_products(request):
    products = Product.objects.all()
    form = ProductForm()
    context ={
        "products": products,
        "form":form,
    }
    return render(request,"admin/products.html",context)
@login_required_superadmin_required
def admin_view_customers(request):
    customers = Customer.objects.all()
    form = CustomerCreationForm()

    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully!")
            return redirect("store:admin_view_customers")
        else:
            messages.error(request, "There was an error adding the Customer. Please check the form.")
         
    if 'inid' in request.GET:
        customer_id = request.GET['inid']
        customer = get_object_or_404(Customer, pk=customer_id)
        customer.status = False
        customer.save()
        messages.error(request, f"{customer.user.first_name} {customer.user.last_name} Has beed deactivated!")
        return redirect('store:admin_view_customers')

    if 'id' in request.GET:
        customer_id = request.GET['id']
        customer = get_object_or_404(Customer, pk=customer_id)
        customer.status = True
        customer.save()
        messages.success(request, f"{customer.user.first_name} {customer.user.last_name} Has beed Activated!")

        return redirect('store:admin_view_customers')
    context ={
        "customers": customers,
        "form": form,
    }
    return render(request,"admin/customers.html",context)
@login_required_superadmin_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        try:
            # Update User model fields
            user = customer.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.save()
            
            # Update Customer model fields
            customer.email = request.POST.get('email', '')
            customer.phone_no = request.POST.get('phone_no', '')
            customer.name = f"{user.first_name} {user.last_name}"
            customer.save()
            
            messages.success(request, f'Customer {customer.name} updated successfully!')
            return redirect('store:admin_view_customers')
            
        except Exception as e:
            messages.error(request, f'Error updating customer: {str(e)}')
            return redirect('store:admin_view_customers')
    
    # If GET request, redirect to customer list (the modal will handle display)
    return redirect('store:admin_view_customers')

@login_required_superadmin_required
def admin_view_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'admin/products.html', {
        'products': products,
        'categories': categories,
        'form': ProductForm(),
        'category_form': CategoryForm()
    })

@login_required_superadmin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('store:admin_view_products')
        else:
            messages.error(request, 'Error adding product. Please check the form.')
    return redirect('store:admin_view_products')

@login_required_superadmin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('store:admin_view_products')
        else:
            messages.error(request, 'Error updating product. Please check the form.')
    return redirect('store:admin_view_products')

@login_required_superadmin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
        else:
            messages.error(request, 'Error adding category. Please check the form.')
    return redirect('store:admin_view_products')

@login_required_superadmin_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
        else:
            messages.error(request, 'Error updating category. Please check the form.')
    return redirect('store:admin_view_products')

@login_required_superadmin_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    try:
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting category: {str(e)}')
    return redirect('store:admin_view_products')

@login_required_superadmin_required
def admin_view_orders(request):
    orders = Order.objects.annotate(
        total_value=Sum(F('orderitem__product__price') * F('orderitem__quantity')),
        item_count=Sum('orderitem__quantity')
    ).order_by('-date_ordered')
    
    today = timezone.now().date()
    recent_orders = orders.filter(date_ordered__date=today)
    total_revenue = orders.aggregate(total=Sum('total_value'))['total'] or 0
    
    context = {
        'orders': orders,
        'recent_orders_count': recent_orders.count(),
        'total_revenue': total_revenue,
        'today': today,
    }
    return render(request, 'admin/orders.html', context)

@login_required_superadmin_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('customer', 'shippingaddress')
                    .prefetch_related('orderitem_set__product'), 
        id=order_id
    )
    
    order_items = order.orderitem_set.all()
    context = {
        'order': order,
        'order_items': order_items,
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'admin/order_detail_partial.html', context)
    
    return render(request, 'admin/order_detail.html', context)

@require_POST
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.complete:
        order.complete = True
        order.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Order already completed'})

@login_required_superadmin_required
def update_profile2(request):
    user = request.user 
    if request.method == "POST":
        first_name = request.POST.get("first_name", user.first_name)
        last_name = request.POST.get("last_name", user.last_name)
        password = request.POST.get("password")

        user.first_name = first_name
        user.last_name = last_name
        
        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect("store:update_profile2")

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("store:update_profile2")

    return render(request, "admin/update_profile.html", {"user": user ,"title":"Update Profile"})

def logout(request):
    auth.logout(request)
    messages.info(request,"Logged out successfully!")
    return redirect('login')