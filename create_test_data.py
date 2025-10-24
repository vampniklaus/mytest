#!/usr/bin/env python
"""
创建合理的测试数据脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'used_car_system.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from cars.models import Car, Brand, CarType
from users.models import CustomUser
from ai_recommendation.models import UserPreference

def cleanup_invalid_data():
    """清理不合理的数据"""
    print("=== 清理不合理数据 ===")
    
    # 删除年份不合理的数据
    invalid_cars = Car.objects.filter(year__gt=2024) | Car.objects.filter(year__lt=2000)
    print(f"删除年份不合理的车辆: {invalid_cars.count()} 辆")
    invalid_cars.delete()
    
    # 删除价格不合理的数据
    invalid_price_cars = Car.objects.filter(current_price__gt=10000000) | Car.objects.filter(current_price__lt=10000)
    print(f"删除价格不合理的车辆: {invalid_price_cars.count()} 辆")
    invalid_price_cars.delete()
    
    # 删除重复的测试数据
    test_cars = Car.objects.filter(model='测试车型')
    if test_cars.count() > 1:
        # 保留第一辆，删除其他重复的
        first_car = test_cars.first()
        test_cars.exclude(id=first_car.id).delete()
        print(f"删除重复测试车辆，保留1辆")

def create_realistic_cars():
    """创建合理的车辆数据"""
    print("\\n=== 创建合理的车辆数据 ===")
    
    # 获取品牌和车型
    toyota = Brand.objects.get(name='丰田')
    honda = Brand.objects.get(name='本田')
    volkswagen = Brand.objects.get(name='大众')
    bmw = Brand.objects.get(name='宝马')
    benz = Brand.objects.get(name='奔驰')
    audi = Brand.objects.get(name='奥迪')
    
    sedan = CarType.objects.get(name='轿车')
    suv = CarType.objects.get(name='SUV')
    mpv = CarType.objects.get(name='MPV')
    
    # 获取管理员用户
    admin_user = CustomUser.objects.get(username='test')
    
    # 合理的车辆数据
    realistic_cars = [
        # 丰田系列
        {
            'brand': toyota, 'car_type': sedan, 'model': '卡罗拉', 'year': 2021,
            'mileage': 35000, 'color': '白色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 1.8,
            'original_price': 128000, 'current_price': 98000,
            'description': '2021款丰田卡罗拉，车况良好，无事故，保养记录齐全'
        },
        {
            'brand': toyota, 'car_type': suv, 'model': 'RAV4荣放', 'year': 2020,
            'mileage': 45000, 'color': '黑色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 2.0,
            'original_price': 198000, 'current_price': 158000,
            'description': '2020款丰田RAV4荣放，四驱豪华版，配置丰富，车况精品'
        },
        
        # 本田系列
        {
            'brand': honda, 'car_type': sedan, 'model': '雅阁', 'year': 2022,
            'mileage': 18000, 'color': '银色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 1.5,
            'original_price': 189800, 'current_price': 165000,
            'description': '2022款本田雅阁，准新车，行驶里程少，车况完美'
        },
        {
            'brand': honda, 'car_type': suv, 'model': 'CR-V', 'year': 2019,
            'mileage': 68000, 'color': '白色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 1.5,
            'original_price': 219800, 'current_price': 168000,
            'description': '2019款本田CR-V，空间大，油耗低，家用首选'
        },
        
        # 大众系列
        {
            'brand': volkswagen, 'car_type': sedan, 'model': '帕萨特', 'year': 2020,
            'mileage': 52000, 'color': '黑色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 1.8,
            'original_price': 215800, 'current_price': 172000,
            'description': '2020款大众帕萨特，商务家用两相宜，配置豪华'
        },
        {
            'brand': volkswagen, 'car_type': suv, 'model': '途观L', 'year': 2021,
            'mileage': 32000, 'color': '棕色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 2.0,
            'original_price': 278000, 'current_price': 228000,
            'description': '2021款大众途观L，空间宽敞，动力强劲，适合家庭出游'
        },
        
        # 宝马系列
        {
            'brand': bmw, 'car_type': sedan, 'model': '3系', 'year': 2021,
            'mileage': 28000, 'color': '蓝色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 2.0,
            'original_price': 328000, 'current_price': 278000,
            'description': '2021款宝马3系，操控性能优秀，驾驶体验极佳'
        },
        
        # 奔驰系列
        {
            'brand': benz, 'car_type': sedan, 'model': 'C级', 'year': 2022,
            'mileage': 15000, 'color': '白色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 1.5,
            'original_price': 348000, 'current_price': 298000,
            'description': '2022款奔驰C级，豪华内饰，科技配置丰富'
        },
        
        # 奥迪系列
        {
            'brand': audi, 'car_type': suv, 'model': 'Q5L', 'year': 2021,
            'mileage': 38000, 'color': '灰色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 2.0,
            'original_price': 398000, 'current_price': 328000,
            'description': '2021款奥迪Q5L，四驱系统，科技感十足，性价比高'
        },
        
        # 经济型车辆
        {
            'brand': honda, 'car_type': sedan, 'model': '飞度', 'year': 2019,
            'mileage': 58000, 'color': '黄色', 'transmission': 'automatic',
            'fuel_type': 'gasoline', 'engine_capacity': 1.5,
            'original_price': 86800, 'current_price': 68000,
            'description': '2019款本田飞度，经济实用，油耗低，适合城市代步'
        },
        
        # 商务车型
        {
            'brand': benz, 'car_type': mpv, 'model': 'V级', 'year': 2020,
            'mileage': 42000, 'color': '黑色', 'transmission': 'automatic',
            'fuel_type': 'diesel', 'engine_capacity': 2.0,
            'original_price': 488000, 'current_price': 398000,
            'description': '2020款奔驰V级，豪华商务MPV，空间宽敞，配置高端'
        }
    ]
    
    created_count = 0
    for car_data in realistic_cars:
        # 检查是否已存在相同车型
        existing = Car.objects.filter(
            brand=car_data['brand'],
            model=car_data['model'],
            year=car_data['year']
        ).exists()
        
        if not existing:
            car = Car.objects.create(
                brand=car_data['brand'],
                car_type=car_data['car_type'],
                model=car_data['model'],
                year=car_data['year'],
                mileage=car_data['mileage'],
                color=car_data['color'],
                transmission=car_data['transmission'],
                fuel_type=car_data['fuel_type'],
                engine_capacity=car_data['engine_capacity'],
                original_price=car_data['original_price'],
                current_price=car_data['current_price'],
                description=car_data['description'],
                seller=admin_user,
                status='approved'
            )
            created_count += 1
            print(f"创建车辆: {car.brand.name} {car.model} ({car.year})")
    
    print(f"成功创建 {created_count} 辆合理车辆")

def create_user_preferences():
    """为用户创建偏好设置"""
    print("\\n=== 创建用户偏好设置 ===")
    
    users = CustomUser.objects.all()
    brands = Brand.objects.all()
    car_types = CarType.objects.all()
    
    for user in users:
        # 创建或获取用户偏好
        preference, created = UserPreference.objects.get_or_create(user=user)
        
        # 设置合理的偏好
        if created:
            # 随机选择2-3个品牌偏好
            preferred_brands = list(brands.order_by('?')[:3])
            preference.preferred_brands.set(preferred_brands)
            
            # 随机选择1-2个车型偏好
            preferred_types = list(car_types.order_by('?')[:2])
            preference.preferred_types.set(preferred_types)
            
            # 设置预算范围（随机选择）
            budget_choices = ['5-10', '10-20', '20-50']
            preference.budget_range = budget_choices[user.id % len(budget_choices)]
            
            # 设置最小年份（2018-2021）
            preference.min_year = 2018 + (user.id % 4)
            
            # 设置最大里程（5-15万公里）
            preference.max_mileage = 5 + (user.id % 11)
            
            preference.save()
            print(f"为用户 {user.username} 创建偏好设置")

def main():
    """主函数"""
    print("开始创建测试数据...")
    
    # 清理不合理数据
    cleanup_invalid_data()
    
    # 创建合理的车辆数据
    create_realistic_cars()
    
    # 创建用户偏好设置
    create_user_preferences()
    
    # 统计最终数据
    print("\\n=== 最终数据统计 ===")
    print(f"车辆总数: {Car.objects.count()}")
    print(f"已审核车辆: {Car.objects.filter(status='approved').count()}")
    print(f"用户偏好设置: {UserPreference.objects.count()}")
    
    print("\\n测试数据创建完成！")

if __name__ == '__main__':
    main()