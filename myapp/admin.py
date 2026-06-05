from django.contrib import admin
from myapp.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(MyQRCode)
admin.site.register(CartItem)
admin.site.register(ContactUs)
admin.site.register(UserProfile)


# backend/services/admin.py
from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'is_active', 'order', 'created_at']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    fieldsets = (
        ('Service Information', {
            'fields': ('title', 'description', 'icon', 'icon_color')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )



from django.contrib import admin
from .models import (
    Product, CartItem, MyQRCode, ContactUs,
    UserProfile, Service, Order, OrderItem  # new imports
)

# ----- Existing admin registrations (if any) -----
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discounted_price']
    search_fields = ['name']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'added_at']

@admin.register(MyQRCode)
class MyQRCodeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']


# ========== New Order & OrderItem Admin ==========
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # don't show empty extra rows
    readonly_fields = ['product_name', 'product_price', 'quantity', 'product_image']
    fields = ['product', 'product_name', 'product_price', 'quantity', 'product_image']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'total_amount', 'status',
        'transaction_id', 'created_at', 'phone'
    ]
    list_filter = ['status', 'created_at', 'state']
    search_fields = ['id', 'user__username', 'transaction_id', 'phone', 'address_line1']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Customer & Status', {
            'fields': ('user', 'status', 'total_amount', 'transaction_id', 'payment_screenshot')
        }),
        ('Shipping Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'pincode', 'landmark', 'phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [OrderItemInline]
    actions = ['mark_as_verified', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'cancel_orders']

    # Custom admin actions to quickly change status
    def mark_as_verified(self, request, queryset):
        queryset.update(status='VERIFIED')
    mark_as_verified.short_description = "Mark selected as Payment Verified"

    def mark_as_processing(self, request, queryset):
        queryset.update(status='PROCESSING')
    mark_as_processing.short_description = "Mark selected as Processing"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')
    mark_as_shipped.short_description = "Mark selected as Shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')
    mark_as_delivered.short_description = "Mark selected as Delivered"

    def cancel_orders(self, request, queryset):
        queryset.update(status='CANCELLED')
    cancel_orders.short_description = "Cancel selected orders"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'product_name', 'quantity', 'product_price']
    search_fields = ['product_name', 'order__id']