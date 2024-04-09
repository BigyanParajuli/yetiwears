from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=55)
    slug = models.SlugField(max_length=55)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name



    
class Product(models.Model):
    user = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
    
    def __str__(self):
        return self.title
    
