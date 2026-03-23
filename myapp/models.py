from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.TextField()
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="myimages")

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class MyQRCode(models.Model):
    name = models.CharField(max_length=50)
    qr = models.FileField(upload_to="myqrcode")
    def __str__(self):
         return self.name



class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField(max_length=100)
    def __str__(self):
        return self.name
    


from django.db import models
from django.contrib.auth.models import User

# Yeh model User ke saath automatically connect hoga
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username




# backend/services/models.py
from django.db import models
from django.utils import timezone

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class (e.g., bi-cart-check-fill)")
    icon_color = models.CharField(max_length=20, default="text-primary", help_text="Text color class")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title