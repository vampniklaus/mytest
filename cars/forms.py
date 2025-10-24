from django import forms
from .models import Car, CarImage, CarFeature, Brand, CarType

class CarForm(forms.ModelForm):
    """车辆上架表单"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置品牌和类型的下拉选择
        self.fields['brand'].queryset = Brand.objects.all()
        self.fields['car_type'].queryset = CarType.objects.all()
        
        # 添加样式类
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = Car
        fields = [
            'brand', 'car_type', 'model', 'year', 'mileage',
            'color', 'transmission', 'fuel_type', 'engine_capacity',
            'original_price', 'current_price', 'description', 'main_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'min': 1990, 'max': 2025}),
            'mileage': forms.NumberInput(attrs={'min': 0, 'step': 0.1}),
            'engine_capacity': forms.NumberInput(attrs={'min': 0.5, 'max': 8.0, 'step': 0.1}),
            'original_price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
            'current_price': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }

class CarImageForm(forms.ModelForm):
    """车辆图片表单"""
    
    class Meta:
        model = CarImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CarFeatureForm(forms.ModelForm):
    """车辆特性表单"""
    
    class Meta:
        model = CarFeature
        fields = ['feature_name', 'feature_value']
        widgets = {
            'feature_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '如：空调类型'}),
            'feature_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '如：自动空调'}),
        }

CarImageFormSet = forms.inlineformset_factory(
    Car, CarImage, form=CarImageForm, extra=3, can_delete=True
)

CarFeatureFormSet = forms.inlineformset_factory(
    Car, CarFeature, form=CarFeatureForm, extra=3, can_delete=True
)