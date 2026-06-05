from django.contrib import admin
from myapp.models import Product, CartItem, MyQRCode, ContactUs, UserProfile, Order, OrderItem

# ---------- Existing models (simple registration) ----------
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(MyQRCode)
admin.site.register(ContactUs)
admin.site.register(UserProfile)

# ---------- OrderItem Inline ----------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'product_image']
    fields = ['product', 'product_name', 'product_price', 'quantity', 'product_image']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

# ---------- Order Admin ----------
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
    actions = [
        'mark_as_verified', 'mark_as_processing', 'mark_as_shipped',
        'mark_as_delivered', 'cancel_orders'
    ]

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

# ---------- OrderItem Admin (optional) ----------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'product_name', 'quantity', 'product_price']
    search_fields = ['product_name', 'order__id']