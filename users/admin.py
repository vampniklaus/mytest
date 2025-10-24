from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, FavoriteCar

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'user_type', 'is_verified', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_verified', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {
            'fields': ('phone', 'user_type', 'avatar', 'is_verified')
        }),
        ('卖家信息', {
            'fields': ('seller_license', 'seller_address', 'seller_description'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'real_name', 'id_card')
    search_fields = ('user__username', 'real_name', 'id_card')

@admin.register(FavoriteCar)
class FavoriteCarAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'car__brand', 'car__model')