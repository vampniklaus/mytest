from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserPreference(models.Model):
    """用户偏好设置"""
    
    BUDGET_CHOICES = [
        ('0-5', '0-5万'),
        ('5-10', '5-10万'),
        ('10-20', '10-20万'),
        ('20-50', '20-50万'),
        ('50+', '50万以上'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preferences')
    
    # 基本偏好
    preferred_brands = models.ManyToManyField('cars.Brand', blank=True, verbose_name=_('偏好品牌'))
    preferred_types = models.ManyToManyField('cars.CarType', blank=True, verbose_name=_('偏好类型'))
    budget_range = models.CharField(_('预算范围'), max_length=10, choices=BUDGET_CHOICES, default='10-20')
    
    # 详细偏好
    min_year = models.IntegerField(_('最小年份'), default=2015)
    max_mileage = models.DecimalField(_('最大里程'), max_digits=10, decimal_places=2, default=100000)
    preferred_fuel_types = models.JSONField(_('偏好燃料类型'), default=list)
    preferred_transmissions = models.JSONField(_('偏好变速箱'), default=list)
    
    # AI学习数据
    search_history = models.JSONField(_('搜索历史'), default=list)
    click_history = models.JSONField(_('点击历史'), default=list)
    favorite_categories = models.JSONField(_('收藏类别'), default=list)
    
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('用户偏好')
        verbose_name_plural = _('用户偏好')
    
    def __str__(self):
        return f"{self.user.username}的偏好设置"

class AIRecommendation(models.Model):
    """AI推荐记录"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_recommendations')
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, verbose_name=_('推荐车辆'))
    
    # 推荐参数
    recommendation_reason = models.TextField(_('推荐理由'))
    match_score = models.DecimalField(_('匹配度'), max_digits=5, decimal_places=2, default=0)
    
    # 用户反馈
    is_viewed = models.BooleanField(_('是否查看'), default=False)
    is_clicked = models.BooleanField(_('是否点击'), default=False)
    user_rating = models.IntegerField(_('用户评分'), null=True, blank=True)
    
    created_at = models.DateTimeField(_('推荐时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('AI推荐')
        verbose_name_plural = _('AI推荐')
        ordering = ['-match_score']
    
    def __str__(self):
        return f"{self.user.username}的推荐: {self.car.brand.name} {self.car.model}"

class PricePrediction(models.Model):
    """价格预测记录"""
    car = models.OneToOneField('cars.Car', on_delete=models.CASCADE, related_name='price_prediction')
    
    # 预测数据
    predicted_price = models.DecimalField(_('预测价格'), max_digits=12, decimal_places=2)
    confidence_score = models.DecimalField(_('置信度'), max_digits=5, decimal_places=2, default=0)
    
    # 市场分析
    market_trend = models.CharField(_('市场趋势'), max_length=20, choices=[
        ('rising', '上涨'),
        ('stable', '稳定'),
        ('declining', '下跌'),
    ])
    
    # 影响因素
    influencing_factors = models.JSONField(_('影响因素'), default=list)
    
    created_at = models.DateTimeField(_('预测时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('价格预测')
        verbose_name_plural = _('价格预测')
    
    def __str__(self):
        return f"{self.car.brand.name} {self.car.model}价格预测"

class AITrainingData(models.Model):
    """AI训练数据"""
    data_type = models.CharField(_('数据类型'), max_length=50, choices=[
        ('car_features', '车辆特征'),
        ('price_history', '价格历史'),
        ('user_behavior', '用户行为'),
        ('market_data', '市场数据'),
    ])
    
    data_content = models.JSONField(_('数据内容'))
    data_source = models.CharField(_('数据来源'), max_length=100)
    is_processed = models.BooleanField(_('是否已处理'), default=False)
    
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('AI训练数据')
        verbose_name_plural = _('AI训练数据')
    
    def __str__(self):
        return f"{self.data_type} - {self.data_source}"