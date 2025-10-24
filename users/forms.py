from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    """用户注册表单"""
    email = forms.EmailField(required=True, label='邮箱地址')
    phone = forms.CharField(max_length=15, required=True, label='手机号码')
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES, 
        initial='buyer',
        label='用户类型'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'user_type', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('该手机号已被注册')
        return phone

class UserLoginForm(AuthenticationForm):
    """用户登录表单"""
    username = forms.CharField(label='用户名/邮箱/手机号')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # 支持用户名、邮箱、手机号登录
        return username

class UserProfileForm(forms.ModelForm):
    """用户资料表单"""
    class Meta:
        model = UserProfile
        fields = ['real_name', 'id_card', 'address']
        labels = {
            'real_name': '真实姓名',
            'id_card': '身份证号',
            'address': '联系地址',
        }
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class SellerRegistrationForm(forms.ModelForm):
    """卖家注册表单"""
    password1 = forms.CharField(widget=forms.PasswordInput, label='密码')
    password2 = forms.CharField(widget=forms.PasswordInput, label='确认密码')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'seller_license', 'seller_address', 'seller_description']
        labels = {
            'username': '用户名',
            'email': '邮箱地址',
            'phone': '手机号码',
            'seller_license': '营业执照',
            'seller_address': '商家地址',
            'seller_description': '商家描述',
        }
        widgets = {
            'seller_address': forms.Textarea(attrs={'rows': 3}),
            'seller_description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.user_type = 'seller'
        if commit:
            user.save()
        return user