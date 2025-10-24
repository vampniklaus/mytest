from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from cars.models import Car, Brand, CarType
from .models import UserPreference, AIRecommendation
import json

@login_required
def ai_recommendation(request):
    """AI推荐页面"""
    # 获取品牌和车型数据用于前端显示
    brands = Brand.objects.all()
    car_types = CarType.objects.all()
    
    # 获取用户已有的偏好设置
    try:
        user_preference = UserPreference.objects.get(user=request.user)
    except UserPreference.DoesNotExist:
        user_preference = None
    
    return render(request, 'ai_recommendation/recommendation.html', {
        'brands': brands,
        'car_types': car_types,
        'user_preference': user_preference
    })

@login_required
@require_http_methods(["POST"])
def save_preferences(request):
    """保存用户偏好设置"""
    try:
        data = json.loads(request.body)
        
        # 创建或更新用户偏好
        user_preference, created = UserPreference.objects.get_or_create(user=request.user)
        
        # 更新偏好设置
        user_preference.budget_range = data.get('budget_range', '10-20')
        user_preference.min_year = int(data.get('min_year', 2015))
        user_preference.max_mileage = float(data.get('max_mileage', 10))
        
        # 清空之前的品牌和车型偏好
        user_preference.preferred_brands.clear()
        user_preference.preferred_types.clear()
        
        # 添加新的品牌偏好
        preferred_brand_ids = data.get('preferred_brands', [])
        for brand_id in preferred_brand_ids:
            try:
                brand = Brand.objects.get(id=int(brand_id))
                user_preference.preferred_brands.add(brand)
            except Brand.DoesNotExist:
                pass
        
        # 添加新的车型偏好
        preferred_type_ids = data.get('preferred_types', [])
        for type_id in preferred_type_ids:
            try:
                car_type = CarType.objects.get(id=int(type_id))
                user_preference.preferred_types.add(car_type)
            except CarType.DoesNotExist:
                pass
        
        user_preference.save()
        
        return JsonResponse({'status': 'success', 'message': '偏好设置已保存'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@require_http_methods(["GET"])
def get_recommendations(request):
    """获取AI推荐结果"""
    try:
        # 获取用户偏好
        try:
            user_preference = UserPreference.objects.get(user=request.user)
        except UserPreference.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '请先设置偏好'})
        
        # 获取所有已审核的车辆
        cars = Car.objects.filter(status='approved')
        
        # 根据偏好筛选车辆
        filtered_cars = []
        
        for car in cars:
            # 计算匹配度
            match_score = 0
            reasons = []
            
            # 品牌匹配
            if user_preference.preferred_brands.filter(id=car.brand.id).exists():
                match_score += 30
                reasons.append('符合您的品牌偏好')
            
            # 车型匹配
            if user_preference.preferred_types.filter(id=car.car_type.id).exists():
                match_score += 25
                reasons.append('符合您的车型偏好')
            
            # 年份匹配（过滤掉不合理的年份）
            if car.year >= user_preference.min_year and car.year <= 2024:
                match_score += 20
                reasons.append('年份符合要求')
            
            # 里程匹配（将公里转换为万公里进行比较）
            car_mileage_wan = float(car.mileage) / 10000  # 转换为万公里
            if car_mileage_wan <= float(user_preference.max_mileage):
                match_score += 15
                reasons.append('里程数在可接受范围内')
            
            # 预算匹配（处理价格范围）
            budget_min, budget_max = user_preference.budget_range.split('-')
            budget_min = float(budget_min) if budget_min != '50+' else 50
            budget_max = float(budget_max) if budget_max != '+' else float('inf')
            
            # 将价格转换为万元进行比较
            car_price_wan = float(car.current_price) / 10000
            
            if budget_min <= car_price_wan <= budget_max:
                match_score += 10
                reasons.append('价格在预算范围内')
            
            # 如果没有任何匹配，给予基础分
            if match_score == 0:
                match_score = 10  # 基础推荐分
                reasons.append('为您推荐的热门车辆')
            
            # 降低匹配度要求，显示更多车辆
            if match_score >= 20:  # 降低到20分就显示
                filtered_cars.append({
                    'car': car,
                    'match_score': match_score,
                    'reasons': reasons
                })
        
        # 按匹配度排序
        filtered_cars.sort(key=lambda x: x['match_score'], reverse=True)
        
        # 准备推荐结果
        recommendations = []
        for item in filtered_cars[:6]:  # 最多显示6个推荐
            car = item['car']
            
            # 创建推荐记录
            recommendation, created = AIRecommendation.objects.get_or_create(
                user=request.user,
                car=car,
                defaults={
                    'recommendation_reason': '，'.join(item['reasons']),
                    'match_score': item['match_score']
                }
            )
            
            # 将价格转换为万元显示
            car_price_wan = float(car.current_price) / 10000
            
            recommendations.append({
                'id': car.id,
                'brand': car.brand.name if car.brand else '未知品牌',
                'model': car.model,
                'year': car.year,
                'mileage': f"{float(car.mileage) / 10000:.1f}",  # 显示为万公里
                'price': f"{car_price_wan:.1f}",  # 显示为万元
                'matchScore': item['match_score'],
                'reason': '，'.join(item['reasons']),
                'main_image': car.main_image.url if car.main_image else '/static/images/default-car.svg'
            })
        
        return JsonResponse({
            'status': 'success',
            'recommendations': recommendations,
            'total_count': len(recommendations)
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@require_http_methods(["GET"])
def get_recommendation_history(request):
    """获取推荐历史"""
    try:
        recommendations = AIRecommendation.objects.filter(user=request.user).order_by('-created_at')[:10]
        
        history_data = []
        for rec in recommendations:
            history_data.append({
                'car_brand': rec.car.brand.name if rec.car.brand else '未知品牌',
                'car_model': rec.car.model,
                'match_score': float(rec.match_score),
                'reason': rec.recommendation_reason,
                'created_at': rec.created_at.strftime('%Y-%m-%d %H:%M'),
                'is_viewed': rec.is_viewed,
                'is_clicked': rec.is_clicked
            })
        
        return JsonResponse({'status': 'success', 'history': history_data})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})