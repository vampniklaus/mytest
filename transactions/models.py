from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Transaction(models.Model):
    """交易订单"""
    
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('confirmed', '卖家确认'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
        ('bank', '银行转账'),
        ('cash', '现金'),
    ]
    
    # 订单基本信息
    order_number = models.CharField(_('订单号'), max_length=20, unique=True)
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name=_('车辆'))
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('买家'), related_name='purchases')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('卖家'), related_name='sales')
    
    # 价格信息
    final_price = models.DecimalField(_('成交价格'), max_digits=12, decimal_places=2)
    deposit = models.DecimalField(_('定金'), max_digits=12, decimal_places=2, default=0)
    
    # 交易状态
    status = models.CharField(_('订单状态'), max_length=15, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(_('支付方式'), max_length=10, choices=PAYMENT_METHOD_CHOICES)
    
    # 时间信息
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    paid_at = models.DateTimeField(_('支付时间'), null=True, blank=True)
    confirmed_at = models.DateTimeField(_('确认时间'), null=True, blank=True)
    shipped_at = models.DateTimeField(_('发货时间'), null=True, blank=True)
    delivered_at = models.DateTimeField(_('送达时间'), null=True, blank=True)
    completed_at = models.DateTimeField(_('完成时间'), null=True, blank=True)
    cancelled_at = models.DateTimeField(_('取消时间'), null=True, blank=True)
    
    # 物流信息
    shipping_address = models.TextField(_('收货地址'))
    tracking_number = models.CharField(_('物流单号'), max_length=50, blank=True, null=True)
    shipping_company = models.CharField(_('物流公司'), max_length=100, blank=True, null=True)
    
    # 备注信息
    buyer_notes = models.TextField(_('买家备注'), blank=True, null=True)
    seller_notes = models.TextField(_('卖家备注'), blank=True, null=True)
    cancellation_reason = models.TextField(_('取消原因'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('交易订单')
        verbose_name_plural = _('交易订单')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"订单 {self.order_number} - {self.car.brand.name} {self.car.model}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # 生成订单号
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.order_number = f"OC{timestamp}"
        super().save(*args, **kwargs)

class TransactionHistory(models.Model):
    """交易历史记录"""
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(_('状态'), max_length=15)
    notes = models.TextField(_('备注'), blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('操作人'))
    created_at = models.DateTimeField(_('操作时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('交易历史')
        verbose_name_plural = _('交易历史')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction.order_number} - {self.status}"

class Review(models.Model):
    """交易评价"""
    
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, verbose_name=_('交易'))
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('评价人'))
    reviewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('被评价人'), related_name='reviews_received')
    rating = models.IntegerField(_('评分'), choices=RATING_CHOICES)
    comment = models.TextField(_('评价内容'))
    is_anonymous = models.BooleanField(_('匿名评价'), default=False)
    created_at = models.DateTimeField(_('评价时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('交易评价')
        verbose_name_plural = _('交易评价')
        unique_together = ('transaction', 'reviewer')
    
    def __str__(self):
        return f"{self.reviewer.username}对{self.reviewed_user.username}的评价"