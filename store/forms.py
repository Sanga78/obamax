from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from .models import Category, Customer, Product,ProductReview
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'stock', 
                 'image', 'digital', 'discount_percentage',
                 'flash_sale_price', 'flash_sale_start_time', 'flash_sale_end_time']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'flash_sale_start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'flash_sale_end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['flash_sale_price'].required = False
        self.fields['flash_sale_start_time'].required = False
        self.fields['flash_sale_end_time'].required = False

class CustomerCreationForm(UserCreationForm):
    phone_no = forms.CharField(
        max_length=20, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                phone_no=self.cleaned_data['phone_no'],
                name=f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}",
                email=self.cleaned_data['email'],
                status=True  # Set status to True by default
            )
        return user
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'rating-input'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Summary of your review',
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review here...',
                'rows': 5,
                'class': 'form-control'
            }),
        }