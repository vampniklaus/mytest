from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_list, name='car_list'),
    path('add/', views.CarCreateView.as_view(), name='car_add'),
    path('management/', views.car_management, name='car_management'),
    path('<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_edit'),
    path('<int:car_id>/', views.car_detail, name='car_detail'),

    # API接口
    path('api/latest/', views.latest_cars_api, name='latest_cars_api'),
    path('api/brands/', views.brands_api, name='brands_api'),
    path('api/car-types/', views.car_types_api, name='car_types_api'),
    path('api/statistics/', views.statistics_api, name='statistics_api'),
    path('api/statistics/', views.statistics_api, name='statistics_api'),
]