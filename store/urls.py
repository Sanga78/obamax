from .import views
from django.urls import path
app_name = 'store'
urlpatterns = [
    path('cart',views.cart,name="cart"),
    path('about',views.about_page,name="about"),
    path('contact',views.contact_us,name="contact"),
    path('checkout',views.checkout,name="checkout"),
    path('<int:product_id>/',views.product_detail,name='product_detail'),
]
