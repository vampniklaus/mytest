from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def ai_recommendation(request):
    """AI推荐页面"""
    return render(request, 'ai_recommendation/recommendation.html')