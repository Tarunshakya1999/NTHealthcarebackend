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