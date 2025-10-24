from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_rooms, name='chat_rooms'),
    path('<int:room_id>/', views.chat_room, name='chat_room'),
]