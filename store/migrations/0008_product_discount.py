# Generated by Django 5.0.7 on 2024-07-27 09:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_customer_phone_no"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="discount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=2),
        ),
    ]
