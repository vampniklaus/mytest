from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_recommendation, name='ai_recommendation'),
    path('save-preferences/', views.save_preferences, name='save_preferences'),
    path('get-recommendations/', views.get_recommendations, name='get_recommendations'),
    path('recommendation-history/', views.get_recommendation_history, name='recommendation_history'),
]