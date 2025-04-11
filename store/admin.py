from django.contrib import admin

from .models import Accesory, Category, Customer, Order, OrderItem, Product,ProductReview

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Accesory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')
    actions = ['approve_reviews', 'unapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"
    
    def unapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_reviews.short_description = "Unapprove selected reviews"