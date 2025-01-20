from .import views
from django.urls import path
app_name = 'store'
urlpatterns = [
    path('',views.index,name="home_page"),
    path('cart',views.cart,name="cart"),
    path('about',views.about_page,name="about"),
    path('contact',views.contact_us,name="contact"),
    path('<int:product_id>/',views.product_detail,name='product_detail'),
    path('search',views.search,name='search'),
    path('update_item',views.updateItem,name='update_item'),
    path('process_order',views.processOrder,name='process_order'),
    path('checkout',views.checkout,name="checkout"),
    path("category/<str:name>", views.category, name="category"),
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    # path('carts/',views.cart_detail,name="cart_detail"),
    # path('add-to-cart/<int:product_id>/',views.add_to_cart,name="add_to_cart"),



    path('admin_home',views.admin_home,name='admin_home'),
    path('products',views.admin_view_products,name='admin_view_products'),
    path('customers',views.admin_view_customers,name='admin_view_customers'),
]
