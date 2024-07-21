from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(null=True,blank=True,upload_to='products/')

    def __str__(self):
        return self.name   

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 
    
class Accesory(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    accesory_type = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField()

    def __str__(self):
        return self.accesory_type