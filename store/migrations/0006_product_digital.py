# Generated by Django 5.0.7 on 2024-07-22 10:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_remove_cartitem_cart_remove_cartitem_product_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="digital",
            field=models.BooleanField(default=False, null=True),
        ),
    ]