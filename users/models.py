from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """自定义用户模型，扩展Django默认用户模型"""
    
    USER_TYPE_CHOICES = [
        ('buyer', '买家'),
        ('seller', '卖家'),
        ('admin', '管理员'),
    ]
    
    phone = models.CharField(_('手机号码'), max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(_('邮箱地址'), unique=True)
    user_type = models.CharField(_('用户类型'), max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
    avatar = models.ImageField(_('头像'), upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(_('是否验证'), default=False)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    # 卖家特有字段
    seller_license = models.CharField(_('营业执照'), max_length=50, blank=True, null=True)
    seller_address = models.TextField(_('商家地址'), blank=True, null=True)
    seller_description = models.TextField(_('商家描述'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class UserProfile(models.Model):
    """用户扩展信息"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    real_name = models.CharField(_('真实姓名'), max_length=50, blank=True, null=True)
    id_card = models.CharField(_('身份证号'), max_length=18, blank=True, null=True)
    address = models.TextField(_('联系地址'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('用户资料')
        verbose_name_plural = _('用户资料')
    
    def __str__(self):
        return f"{self.user.username}的资料"

class FavoriteCar(models.Model):
    """用户收藏的车辆"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('收藏时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('收藏车辆')
        verbose_name_plural = _('收藏车辆')
        unique_together = ('user', 'car')
    
    def __str__(self):
        return f"{self.user.username}收藏的{self.car.brand} {self.car.model}"