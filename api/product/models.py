from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(
        upload_to='category_images/', default="custom_images/no_image.jpg")

    class Meta:
        ordering = (['name'])
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# Creating Product Model


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)

    class Meta:
        ordering = (['created_at'])
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

# Multiple images


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='product_images', on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product.name + " Image"
