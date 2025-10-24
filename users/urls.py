from django.urls import path
from . import views

urlpatterns = [
    # 用户认证
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # 用户资料
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile_edit'),
    
    # 收藏功能
    path('favorites/', views.favorite_cars, name='favorites'),
    path('favorites/toggle/<int:car_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # 交易历史
    path('transactions/', views.transaction_history, name='transaction_history'),
]