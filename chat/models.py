from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class ChatRoom(models.Model):
    """聊天室"""
    
    ROOM_TYPE_CHOICES = [
        ('transaction', '交易聊天'),
        ('customer_service', '客服咨询'),
    ]
    
    room_id = models.CharField(_('房间ID'), max_length=50, unique=True)
    room_type = models.CharField(_('房间类型'), max_length=20, choices=ROOM_TYPE_CHOICES, default='transaction')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ChatParticipant', related_name='chat_rooms')
    transaction = models.ForeignKey('transactions.Transaction', on_delete=models.CASCADE, 
                                  null=True, blank=True, verbose_name=_('关联交易'))
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    
    class Meta:
        verbose_name = _('聊天室')
        verbose_name_plural = _('聊天室')
    
    def __str__(self):
        return f"聊天室 {self.room_id}"

class ChatParticipant(models.Model):
    """聊天室参与者"""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_participants')
    joined_at = models.DateTimeField(_('加入时间'), auto_now_add=True)
    is_active = models.BooleanField(_('是否活跃'), default=True)
    
    class Meta:
        verbose_name = _('聊天参与者')
        verbose_name_plural = _('聊天参与者')
        unique_together = ('room', 'user')
    
    def __str__(self):
        return f"{self.user.username}在{self.room.room_id}"

class Message(models.Model):
    """聊天消息"""
    
    MESSAGE_TYPE_CHOICES = [
        ('text', '文本'),
        ('image', '图片'),
        ('file', '文件'),
        ('system', '系统消息'),
    ]
    
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('发送者'))
    message_type = models.CharField(_('消息类型'), max_length=10, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField(_('消息内容'))
    image = models.ImageField(_('图片'), upload_to='chat_images/', blank=True, null=True)
    file = models.FileField(_('文件'), upload_to='chat_files/', blank=True, null=True)
    is_read = models.BooleanField(_('是否已读'), default=False)
    created_at = models.DateTimeField(_('发送时间'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('聊天消息')
        verbose_name_plural = _('聊天消息')
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"