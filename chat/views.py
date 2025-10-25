from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import ChatRoom, ChatParticipant, Message
from users.models import CustomUser
from cars.models import Car
from transactions.models import Transaction
import json

@login_required
def chat_rooms(request):
    """聊天室列表页面"""
    return render(request, 'chat/chat_rooms.html')

@login_required
def chat_room(request, room_id):
    """聊天室页面"""
    room = get_object_or_404(ChatRoom, room_id=room_id)
    return render(request, 'chat/chat_room.html', {'room': room})

@login_required
@require_http_methods(["GET"])
def get_chat_rooms_api(request):
    """获取用户参与的聊天室列表"""
    user_rooms = ChatRoom.objects.filter(
        chatparticipant__user=request.user,
        chatparticipant__is_active=True
    ).order_by('-updated_at')
    
    rooms_data = []
    for room in user_rooms:
        # 获取最后一条消息
        last_message = room.messages.last()
        # 获取对方用户
        other_participants = room.chatparticipant_set.filter(is_active=True).exclude(user=request.user)
        other_user = other_participants.first().user if other_participants.exists() else None
        
        room_data = {
            'room_id': room.room_id,
            'room_type': room.room_type,
            'room_name': f"与{other_user.username}的聊天" if other_user else "客服聊天",
            'other_user': {
                'username': other_user.username if other_user else "客服",
                'avatar': other_user.avatar.url if other_user and other_user.avatar else '/static/images/default-avatar.png'
            } if other_user else {
                'username': "客服",
                'avatar': '/static/images/default-avatar.png'
            },
            'last_message': {
                'content': last_message.content[:50] + '...' if last_message else '暂无消息',
                'sender': last_message.sender.username if last_message else None,
                'timestamp': last_message.created_at.isoformat() if last_message else room.created_at.isoformat()
            },
            'unread_count': room.messages.filter(is_read=False).exclude(sender=request.user).count(),
            'updated_at': room.updated_at.isoformat()
        }
        rooms_data.append(room_data)
    
    return JsonResponse({'rooms': rooms_data})

@login_required
@require_http_methods(["GET"])
def get_messages_api(request, room_id):
    """获取聊天室消息"""
    room = get_object_or_404(ChatRoom, room_id=room_id)
    # 检查用户是否在聊天室中
    if not room.chatparticipant_set.filter(user=request.user, is_active=True).exists():
        return JsonResponse({'error': '无权访问此聊天室'}, status=403)
    
    messages = room.messages.all().order_by('created_at')
    messages_data = []
    for message in messages:
        message_data = {
            'id': message.id,
            'sender': {
                'id': message.sender.id,
                'username': message.sender.username,
                'avatar': message.sender.avatar.url if message.sender.avatar else '/static/images/default-avatar.png'
            },
            'message_type': message.message_type,
            'content': message.content,
            'image': message.image.url if message.image else None,
            'file': message.file.url if message.file else None,
            'is_read': message.is_read,
            'timestamp': message.created_at.isoformat(),
            'is_own': message.sender == request.user
        }
        messages_data.append(message_data)
    
    # 标记为已读
    room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    return JsonResponse({'messages': messages_data})

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def send_message_api(request, room_id):
    """发送消息"""
    try:
        data = json.loads(request.body)
        room = get_object_or_404(ChatRoom, room_id=room_id)
        
        # 检查用户是否在聊天室中
        if not room.chatparticipant_set.filter(user=request.user, is_active=True).exists():
            return JsonResponse({'error': '无权在此聊天室发送消息'}, status=403)
        
        content = data.get('content', '').strip()
        if not content:
            return JsonResponse({'error': '消息内容不能为空'}, status=400)
        
        message = Message.objects.create(
            room=room,
            sender=request.user,
            message_type='text',
            content=content
        )
        
        # 更新聊天室时间
        room.updated_at = timezone.now()
        room.save()
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'content': message.content,
                'timestamp': message.created_at.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_chat_room_api(request):
    """创建聊天室"""
    try:
        data = json.loads(request.body)
        room_type = data.get('room_type', 'transaction')
        target_user_id = data.get('target_user_id')
        car_id = data.get('car_id')
        
        if room_type == 'transaction' and not (target_user_id and car_id):
            return JsonResponse({'error': '交易聊天室需要目标用户和车辆信息'}, status=400)
        
        # 生成房间ID
        if room_type == 'transaction':
            room_id = f"transaction_{car_id}_{request.user.id}_{target_user_id}"
        else:
            room_id = f"customer_service_{request.user.id}"
        
        # 检查是否已存在聊天室
        room, created = ChatRoom.objects.get_or_create(
            room_id=room_id,
            defaults={
                'room_type': room_type
            }
        )
        
        # 添加参与者
        # 确保当前用户被添加到聊天室中（无论是否新创建）
        ChatParticipant.objects.get_or_create(room=room, user=request.user)
        
        if created:
            # 如果是交易聊天室，添加对方用户
            if room_type == 'transaction' and target_user_id:
                target_user = get_object_or_404(CustomUser, id=target_user_id)
                ChatParticipant.objects.get_or_create(room=room, user=target_user)
                
                # 关联车辆
                if car_id:
                    car = get_object_or_404(Car, id=car_id)
                    room.transaction = Transaction.objects.create(
                        car=car,
                        buyer=request.user,
                        seller=target_user,
                        status='pending'
                    )
                    room.save()
        
        return JsonResponse({
            'success': True,
            'room_id': room.room_id,
            'created': created
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_http_methods(["GET"])
def get_or_create_car_chat(request, car_id):
    """获取或创建车辆相关的聊天室"""
    car = get_object_or_404(Car, id=car_id)
    
    # 检查用户是否有权限（不能和自己聊天）
    if car.seller == request.user:
        return JsonResponse({'error': '不能与自己创建的车辆聊天'}, status=400)
    
    # 生成房间ID
    room_id = f"transaction_{car_id}_{request.user.id}_{car.seller.id}"
    
    # 检查是否已存在聊天室
    room, created = ChatRoom.objects.get_or_create(
        room_id=room_id,
        defaults={
            'room_type': 'transaction'
        }
    )
    
    # 添加参与者
    if created:
        ChatParticipant.objects.get_or_create(room=room, user=request.user)
        ChatParticipant.objects.get_or_create(room=room, user=car.seller)
        
        # 创建交易记录
        room.transaction = Transaction.objects.create(
            car=car,
            buyer=request.user,
            seller=car.seller,
            status='pending'
        )
        room.save()
    
    return JsonResponse({
        'success': True,
        'room_id': room.room_id,
        'created': created,
        'redirect_url': f'/chat/{room.room_id}/'
    })