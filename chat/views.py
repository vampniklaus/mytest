from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat_rooms(request):
    """聊天室列表"""
    return render(request, 'chat/chat_rooms.html')

@login_required
def chat_room(request, room_id):
    """聊天室页面"""
    return render(request, 'chat/chat_room.html', {'room_id': room_id})