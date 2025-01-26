from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["description"].required = False

      class Meta:
          model = Product
          fields = ('description',)
          widgets = {
              "text": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="comments"
              ),
          }