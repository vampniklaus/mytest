from django.contrib import admin
from .models import Brand, CarType, Car, CarImage, CarFeature

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand_type', 'created_at')
    list_filter = ('brand_type', 'created_at')
    search_fields = ('name',)

@admin.register(CarType)
class CarTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name',)

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

class CarFeatureInline(admin.TabularInline):
    model = CarFeature
    extra = 3

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'current_price', 'status', 'seller', 'created_at')
    list_filter = ('status', 'brand', 'car_type', 'year', 'created_at')
    search_fields = ('brand__name', 'model', 'seller__username')
    readonly_fields = ('created_at', 'updated_at', 'approved_at')
    inlines = [CarImageInline, CarFeatureInline]
    
    fieldsets = (
        ('基本信息', {
            'fields': ('brand', 'car_type', 'model', 'year', 'mileage')
        }),
        ('车辆详情', {
            'fields': ('color', 'transmission', 'fuel_type', 'engine_capacity')
        }),
        ('价格信息', {
            'fields': ('original_price', 'current_price', 'ai_suggested_price')
        }),
        ('状态管理', {
            'fields': ('status', 'seller', 'approved_by', 'approved_at', 'rejection_reason')
        }),
        ('图片和描述', {
            'fields': ('main_image', 'description')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.status == 'approved' and not obj.approved_by:
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')

@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    list_display = ('car', 'feature_name', 'feature_value')
    list_filter = ('feature_name',)
    search_fields = ('car__brand__name', 'car__model', 'feature_name')