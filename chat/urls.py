from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # 页面路由
    path('', views.chat_rooms, name='chat_rooms'),
    path('<str:room_id>/', views.chat_room, name='chat_room'),
    
    # API路由
    path('api/rooms/', views.get_chat_rooms_api, name='get_chat_rooms_api'),
    path('api/rooms/create/', views.create_chat_room_api, name='create_chat_room_api'),
    path('api/rooms/car/<int:car_id>/', views.get_or_create_car_chat, name='get_or_create_car_chat'),
    path('api/messages/<str:room_id>/', views.get_messages_api, name='get_messages_api'),
    path('api/messages/<str:room_id>/send/', views.send_message_api, name='send_message_api'),
]