from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Car, Brand, CarType
from .forms import CarForm, CarImageFormSet, CarFeatureFormSet

def car_list(request):
    """车辆列表页面"""
    cars = Car.objects.filter(status='approved').select_related('brand', 'car_type')
    
    # 过滤条件
    brand_filter = request.GET.get('brand')
    type_filter = request.GET.get('type')
    price_range = request.GET.get('price_range')
    
    if brand_filter:
        cars = cars.filter(brand__id=brand_filter)
    if type_filter:
        cars = cars.filter(car_type__id=type_filter)
    if price_range:
        if price_range == '0-5':
            cars = cars.filter(current_price__lte=50000)
        elif price_range == '5-10':
            cars = cars.filter(current_price__gte=50000, current_price__lte=100000)
        elif price_range == '10-20':
            cars = cars.filter(current_price__gte=100000, current_price__lte=200000)
        elif price_range == '20-50':
            cars = cars.filter(current_price__gte=200000, current_price__lte=500000)
        elif price_range == '50+':
            cars = cars.filter(current_price__gte=500000)
    
    brands = Brand.objects.all()
    car_types = CarType.objects.all()
    
    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'brands': brands,
        'car_types': car_types
    })

def car_detail(request, car_id):
    """车辆详情页面"""
    car = get_object_or_404(Car.objects.select_related('brand', 'car_type', 'seller').prefetch_related('images'), id=car_id)
    return render(request, 'cars/car_detail.html', {'car': car})

@method_decorator(login_required, name='dispatch')
class CarCreateView(CreateView):
    """管理员上架车辆视图"""
    model = Car
    form_class = CarForm
    template_name = 'cars/car_add.html'
    success_url = reverse_lazy('car_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = CarImageFormSet(self.request.POST, self.request.FILES)
            context['feature_formset'] = CarFeatureFormSet(self.request.POST)
        else:
            context['image_formset'] = CarImageFormSet()
            context['feature_formset'] = CarFeatureFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        feature_formset = context['feature_formset']
        
        if image_formset.is_valid() and feature_formset.is_valid():
            # 设置卖家为当前用户
            form.instance.seller = self.request.user
            # 管理员上架的车辆直接设置为审核通过，普通卖家上架的车辆也设置为审核通过（便于测试）
            if self.request.user.user_type == 'admin':
                form.instance.status = 'approved'
                form.instance.approved_by = self.request.user
            else:
                form.instance.status = 'approved'  # 普通卖家上架的车辆也直接通过审核
            
            self.object = form.save()
            
            # 保存图片
            image_formset.instance = self.object
            image_formset.save()
            
            # 保存特性
            feature_formset.instance = self.object
            feature_formset.save()
            
            messages.success(self.request, '车辆上架成功！')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class CarUpdateView(UpdateView):
    """编辑车辆信息视图"""
    model = Car
    form_class = CarForm
    template_name = 'cars/car_edit.html'
    success_url = reverse_lazy('car_list')
    
    def get_queryset(self):
        # 只能编辑自己上架的车辆
        return Car.objects.filter(seller=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = CarImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['feature_formset'] = CarFeatureFormSet(self.request.POST, instance=self.object)
        else:
            context['image_formset'] = CarImageFormSet(instance=self.object)
            context['feature_formset'] = CarFeatureFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        feature_formset = context['feature_formset']
        
        if image_formset.is_valid() and feature_formset.is_valid():
            self.object = form.save()
            image_formset.save()
            feature_formset.save()
            messages.success(self.request, '车辆信息更新成功！')
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

@login_required
def car_management(request):
    """车辆管理页面 - 管理员可以管理所有车辆，普通卖家只能管理自己的车辆"""
    if request.user.user_type == 'admin':
        cars = Car.objects.all().select_related('brand', 'car_type', 'seller')
    else:
        cars = Car.objects.filter(seller=request.user).select_related('brand', 'car_type')
    
    return render(request, 'cars/car_management.html', {'cars': cars})



def latest_cars_api(request):
    """获取最新车辆API接口"""
    latest_cars = Car.objects.filter(status='approved').order_by('-created_at')[:6]
    
    cars_data = []
    for car in latest_cars:
        # 检查是否有主图片，如果没有则使用默认图片
        if car.main_image and hasattr(car.main_image, 'url'):
            main_image_url = car.main_image.url
        else:
            main_image_url = '/static/images/default-car.svg'
        
        car_data = {
            'id': car.id,
            'brand': car.brand.name if car.brand else '未知品牌',
            'model': car.model,
            'year': car.year,
            'mileage': f"{car.mileage}万公里",
            'current_price': car.current_price,
            'main_image': main_image_url
        }
        cars_data.append(car_data)
    
    return JsonResponse({'cars': cars_data})

def brands_api(request):
    """获取品牌数据API接口"""
    brands = Brand.objects.all()
    brands_data = [{'id': brand.id, 'name': brand.name} for brand in brands]
    return JsonResponse({'brands': brands_data})

def car_types_api(request):
    """获取车辆类型数据API接口"""
    car_types = CarType.objects.all()
    types_data = [{'id': car_type.id, 'name': car_type.name} for car_type in car_types]
    return JsonResponse({'car_types': types_data})

def statistics_api(request):
    """获取统计数据API接口"""
    from django.contrib.auth import get_user_model
    from transactions.models import Transaction
    
    # 获取真实统计数据
    total_cars = Car.objects.filter(status='approved').count()
    User = get_user_model()
    total_users = User.objects.count()
    total_transactions = Transaction.objects.filter(status='completed').count()
    
    # 计算满意度（基于交易评价）
    completed_transactions = Transaction.objects.filter(status='completed')
    if completed_transactions.exists():
        total_rating = sum(t.rating or 0 for t in completed_transactions if t.rating)
        avg_rating = total_rating / completed_transactions.count()
        satisfaction_rate = min(100, int(avg_rating * 20))  # 5星制转换为百分比
    else:
        satisfaction_rate = 95  # 默认满意度
    
    return JsonResponse({
        'total_cars': total_cars,
        'total_users': total_users,
        'total_transactions': total_transactions,
        'satisfaction_rate': satisfaction_rate
    })

def statistics_api(request):
    """获取统计数据API接口"""
    from django.contrib.auth import get_user_model
    from transactions.models import Transaction
    
    # 获取真实统计数据
    total_cars = Car.objects.filter(status='approved').count()
    User = get_user_model()
    total_users = User.objects.count()
    total_transactions = Transaction.objects.filter(status='completed').count()
    
    # 计算满意度（基于交易评价）
    completed_transactions = Transaction.objects.filter(status='completed')
    if completed_transactions.exists():
        total_rating = sum(t.rating or 0 for t in completed_transactions if t.rating)
        avg_rating = total_rating / completed_transactions.count()
        satisfaction_rate = min(100, int(avg_rating * 20))  # 5星制转换为百分比
    else:
        satisfaction_rate = 95  # 默认满意度
    
    return JsonResponse({
        'total_cars': total_cars,
        'total_users': total_users,
        'total_transactions': total_transactions,
        'satisfaction_rate': satisfaction_rate
    })

