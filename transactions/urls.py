from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('<int:transaction_id>/', views.transaction_detail, name='transaction_detail'),
]