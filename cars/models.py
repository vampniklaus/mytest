from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Brand(models.Model):
    """汽车品牌"""
    
    BRAND_TYPE_CHOICES = [
        ('domestic', '国产品牌'),
        ('imported', '进口品牌'),
    ]
    
    name = models.CharField(_('品牌名称'), max_length=50, unique=True)
    brand_type = models.CharField(_('品牌类型'), max_length=10, choices=BRAND_TYPE_CHOICES, default='domestic')
    logo = models.ImageField(_('品牌Logo'), upload_to='brand_logos/', blank=True, null=True)
    description = models.TextField(_('品牌描述'), blank=True, null=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('汽车品牌')
        verbose_name_plural = _('汽车品牌')
    
    def __str__(self):
        return self.name

class CarType(models.Model):
    """汽车类型"""
    
    TYPE_CATEGORY_CHOICES = [
        ('sedan', '轿车'),
        ('suv', 'SUV'),
        ('mpv', 'MPV'),
        ('coupe', '跑车'),
        ('hatchback', '掀背车'),
        ('wagon', '旅行车'),
        ('pickup', '皮卡'),
    ]
    
    name = models.CharField(_('类型名称'), max_length=50, unique=True)
    category = models.CharField(_('分类'), max_length=20, choices=TYPE_CATEGORY_CHOICES)
    description = models.TextField(_('类型描述'), blank=True, null=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('汽车类型')
        verbose_name_plural = _('汽车类型')
    
    def __str__(self):
        return self.name

class Car(models.Model):
    """车辆信息"""
    
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '审核通过'),
        ('rejected', '审核不通过'),
        ('sold', '已售出'),
        ('maintenance', '维修中'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', '手动'),
        ('automatic', '自动'),
        ('semi_auto', '半自动'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('gasoline', '汽油'),
        ('diesel', '柴油'),
        ('electric', '电动'),
        ('hybrid', '混合动力'),
    ]
    
    # 基本信息
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_('品牌'))
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE, verbose_name=_('类型'))
    model = models.CharField(_('车型'), max_length=100)
    year = models.IntegerField(_('年份'))
    mileage = models.DecimalField(_('里程(公里)'), max_digits=10, decimal_places=2)
    
    # 车辆详情
    color = models.CharField(_('颜色'), max_length=50)
    transmission = models.CharField(_('变速箱'), max_length=10, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(_('燃料类型'), max_length=10, choices=FUEL_TYPE_CHOICES)
    engine_capacity = models.DecimalField(_('排量(L)'), max_digits=4, decimal_places=2)
    
    # 价格信息
    original_price = models.DecimalField(_('原价'), max_digits=12, decimal_places=2)
    current_price = models.DecimalField(_('当前价格'), max_digits=12, decimal_places=2)
    ai_suggested_price = models.DecimalField(_('AI建议价格'), max_digits=12, decimal_places=2, blank=True, null=True)
    
    # 状态管理
    status = models.CharField(_('状态'), max_length=15, choices=STATUS_CHOICES, default='pending')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('卖家'), related_name='cars_for_sale')
    
    # 图片和描述
    main_image = models.ImageField(_('主图'), upload_to='car_images/', blank=True, null=True)
    description = models.TextField(_('车辆描述'))
    
    # 审核信息
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, 
                                   verbose_name=_('审核人'), related_name='approved_cars')
    approved_at = models.DateTimeField(_('审核时间'), null=True, blank=True)
    rejection_reason = models.TextField(_('拒绝原因'), blank=True, null=True)
    
    # 时间戳
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('车辆')
        verbose_name_plural = _('车辆')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})"

class CarImage(models.Model):
    """车辆图片"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('图片'), upload_to='car_images/')
    is_main = models.BooleanField(_('是否主图'), default=False)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('车辆图片')
        verbose_name_plural = _('车辆图片')
    
    def __str__(self):
        return f"{self.car.brand.name} {self.car.model} 图片"

class CarFeature(models.Model):
    """车辆特性"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='features')
    feature_name = models.CharField(_('特性名称'), max_length=100)
    feature_value = models.CharField(_('特性值'), max_length=200)
    
    class Meta:
        verbose_name = _('车辆特性')
        verbose_name_plural = _('车辆特性')
    
    def __str__(self):
        return f"{self.car.brand.name} {self.car.model} - {self.feature_name}"