from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_recommendation, name='ai_recommendation'),
]