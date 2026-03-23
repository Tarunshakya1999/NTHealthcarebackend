from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from myapp.views import *
router = DefaultRouter()
router.register(r'products',ProductViewSets)
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'qrcode',MyQRViewSetAPI, basename='myqr')
router.register(r'contact',ContactUsViewSet, basename='contactus')
router.register(r'services', ServiceViewSet, basename='service')
urlpatterns = [
    path('',include(router.urls)),
    path('cart/update/<int:pk>/', update_cart_item, name='update_cart_item'),  
]
