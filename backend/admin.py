from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Session, Booking

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'oauth_provider', 'is_staff', 'created_at']
    list_filter = ['role', 'oauth_provider', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['created_at', 'updated_at', 'oauth_id', 'oauth_provider']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'avatar', 'bio', 'phone', 'oauth_provider', 'oauth_id', 
                      'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'avatar', 'bio', 'phone')
        }),
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'price', 'duration_minutes', 
                    'status', 'session_type', 'created_at']
    list_filter = ['status', 'session_type', 'category', 'created_at']
    search_fields = ['title', 'description', 'creator__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('creator', 'title', 'description', 'category')
        }),
        ('Session Details', {
            'fields': ('duration_minutes', 'price', 'currency', 'max_attendees', 
                      'location', 'session_type')
        }),
        ('Media', {
            'fields': ('image_url', 'thumbnail_url')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session', 'booking_date', 'attendees_count', 
                    'total_price', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'booking_date', 'created_at']
    search_fields = ['user__username', 'session__title', 'payment_intent_id']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('user', 'session', 'booking_date', 'attendees_count', 'total_price')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Payment Details', {
            'fields': ('payment_intent_id', 'payment_method')
        }),
        ('Notes', {
            'fields': ('user_notes', 'creator_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

