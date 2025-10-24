from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .models import CustomUser, UserProfile, FavoriteCar
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm

class UserRegistrationView(CreateView):
    """用户注册视图"""
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # 自动登录用户
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        messages.success(self.request, '注册成功！欢迎加入二手车交易平台。')
        return response

def user_login(request):
    """用户登录视图"""
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'欢迎回来，{username}！')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    """用户登出视图"""
    logout(request)
    messages.info(request, '您已成功登出。')
    return redirect('home')

@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    """用户资料视图"""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'
    
    def get_object(self):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        # 确保对象被正确设置
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(UpdateView):
    """用户资料更新视图"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('user_profile')
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        messages.success(self.request, '资料更新成功！')
        return super().form_valid(form)

@login_required
def favorite_cars(request):
    """用户收藏车辆列表"""
    favorites = FavoriteCar.objects.filter(user=request.user).select_related('car__brand', 'car__car_type').prefetch_related('car__images')
    return render(request, 'users/favorites.html', {'favorites': favorites, 'user': request.user})

@login_required
def toggle_favorite(request, car_id):
    """添加/移除收藏车辆"""
    from cars.models import Car
    
    car = get_object_or_404(Car, id=car_id)
    favorite, created = FavoriteCar.objects.get_or_create(user=request.user, car=car)
    
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed', 'message': '已从收藏中移除'})
    else:
        return JsonResponse({'status': 'added', 'message': '已添加到收藏'})

@login_required
def transaction_history(request):
    """用户交易历史"""
    from transactions.models import Transaction
    
    purchases = Transaction.objects.filter(buyer=request.user).select_related('car', 'seller')
    sales = Transaction.objects.filter(seller=request.user).select_related('car', 'buyer')
    
    return render(request, 'users/transaction_history.html', {
        'purchases': purchases,
        'sales': sales
    })