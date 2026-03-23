from rest_framework import serializers
from myapp.models import *
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile  # Import UserProfile

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True) # Frontend se phone lena

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")

        return data

    def create(self, validated_data):
        # Phone ko validated_data se nikal lo pehle
        phone = validated_data.pop('phone', None)
        validated_data.pop('password2')
        
        # User create karo
        user = User.objects.create_user(**validated_data)
        
        # Ab phone number UserProfile mein save karo
        # Agar aapne signals use kiye hain toh profile pehle se exist karega
        # Agar nahi kiye toh yahan create karo:
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone = phone
        profile.save()
        
        return user 
from rest_framework import serializers
from .models import CartItem, Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    product_price = serializers.DecimalField(source='product.discounted_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'quantity', 'added_at', 'product_name', 'product_image', 'product_price']
        extra_kwargs = {'user': {'read_only': True}}


class MYQRSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyQRCode
        fields = "__all__"




class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"



# backend/services/serializers.py
from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'icon', 'icon_color', 'is_active', 'order']