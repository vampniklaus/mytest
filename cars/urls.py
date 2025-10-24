from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('add/', views.CarCreateView.as_view(), name='car_add'),
    path('management/', views.car_management, name='car_management'),
    path('<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_edit'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),

]