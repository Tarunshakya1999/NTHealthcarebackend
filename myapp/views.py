from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import *
from .serializer import *

# Product ViewSet
class ProductViewSets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# User Registration View
class RegisterationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "User Registered Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)
        user = self.request.user

        existing_item = CartItem.objects.filter(user=user, product=product).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            serializer.save(user=user)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_cart_item(request, pk):
    try:
        cart_item = CartItem.objects.get(pk=pk, user=request.user)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    action = request.data.get("action")
    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return Response({"message": "Item removed from cart."})
    cart_item.save()
    return Response({"message": "Cart updated"})



class MyQRViewSetAPI(viewsets.ModelViewSet):
    queryset = MyQRCode.objects.all()
    serializer_class = MYQRSerializer




class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer





# backend/services/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Service


@method_decorator(csrf_exempt, name='dispatch')
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_active=True).order_by('order')
    serializer_class = ServiceSerializer
    
    @action(detail=False, methods=['get'])
    def active_services(self, request):
        services = self.get_queryset()
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)
    


import json
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        items_raw = data.get('items', '[]')
        # Frontend JSON string भेज रहा है, parse करो
        if isinstance(items_raw, str):
            items_data = json.loads(items_raw)
        else:
            items_data = items_raw

        # items और empty_cart को data से हटाओ ताकि serializer validate कर सके
        data.pop('items', None)
        empty_cart = data.pop('empty_cart', None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Order items create करो
        for item in items_data:
            product_id = item.pop('product_id', None)
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                    item['product'] = product
                except Product.DoesNotExist:
                    pass
            OrderItem.objects.create(order=order, **item)

        # अगर पूरा cart check out किया है तो cart खाली करो
        if empty_cart == 'true':
            CartItem.objects.filter(user=request.user).delete()

        return Response(OrderSerializer(order, context={'request': request}).data, status=status.HTTP_201_CREATED)

    # ... बाकी actions (update_status, request_return, cancel) पहले जैसे रखो
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response({'status': 'updated'})
        return Response({'error': 'invalid status'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def request_return(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user:
            return Response({'error': 'Not allowed'}, status=403)
        if order.status == 'DELIVERED':
            order.status = 'RETURN_REQUESTED'
            order.save()
            return Response({'status': 'return requested'})
        return Response({'error': 'Order not delivered'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.user != request.user:
            return Response({'error': 'Not allowed'}, status=403)
        if order.status in ['PENDING', 'VERIFIED', 'PROCESSING']:
            order.status = 'CANCELLED'
            order.save()
            return Response({'status': 'cancelled'})
        return Response({'error': 'Cannot cancel'}, status=400)
