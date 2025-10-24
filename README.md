# 二手车交易平台

基于Python Django框架开发的二手车管理系统，提供完整的二手车交易功能。

## 功能特性

### 用户功能模块
- ✅ 用户注册与登录（手机号、邮箱多种方式）
- ✅ 用户信息管理（基本信息修改、交易历史查询、收藏管理）
- ✅ AI智能车辆推荐

### 后台管理模块
- ✅ 品牌与类型录入管理（进口品牌、国产品牌、轿车、SUV等）
- ✅ 品牌与类型查询
- ✅ 用户与车辆审核机制

### 汽车信息管理
- ✅ 车辆基本信息录入（品牌、型号、年份、里程等）
- ✅ 车辆状态跟踪（在售、已售、维修等）
- ✅ AI智能定价与估值

### 卖家功能模块
- ✅ 卖家注册与认证
- ✅ 车辆上架与管理
- ✅ 交易订单管理

### 交易管理模块
- ✅ 订单生成与状态跟踪
- ✅ 在线即时通讯功能

## 技术栈

- **后端**: Python 3.8+, Django 4.2
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **数据库**: SQLite3 (开发), 支持PostgreSQL/MySQL
- **AI功能**: 机器学习价格预测，智能推荐算法
- **实时通讯**: WebSocket (Channels)

## 项目结构

```
used_car_system/
├── used_car_system/          # 项目主配置
├── users/                    # 用户管理应用
├── cars/                     # 车辆管理应用
├── transactions/             # 交易管理应用
├── chat/                     # 聊天功能应用
├── ai_recommendation/        # AI推荐应用
├── templates/                # 前端模板
├── static/                  # 静态文件
├── media/                   # 媒体文件
└── requirements.txt         # 依赖包
```

## 安装和运行

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd used_car_system

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境配置

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑.env文件，配置数据库和API密钥
# SECRET_KEY=your-secret-key
# DEBUG=True
```

### 3. 数据库初始化

```bash
# 生成数据库迁移文件
python manage.py makemigrations

# 应用数据库迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 4. 启动开发服务器

```bash
# 收集静态文件
python manage.py collectstatic

# 启动服务器
python manage.py runserver
```

访问 http://127.0.0.1:8000 查看网站
访问 http://127.0.0.1:8000/admin 进入管理后台

## 主要功能说明

### 用户注册登录
- 支持用户名、邮箱、手机号多种登录方式
- 密码加密存储，确保安全性
- 用户类型分为买家、卖家、管理员

### 车辆管理
- 完整的车辆信息录入界面
- 支持多图片上传
- 车辆状态实时跟踪
- AI智能定价建议

### 交易系统
- 完整的订单生命周期管理
- 多种支付方式支持
- 买卖双方评价系统

### AI推荐功能
- 基于用户行为的智能推荐
- 机器学习价格预测
- 个性化车辆匹配

### 实时聊天
- 买卖双方即时通讯
- 交易相关聊天室
- 客服支持功能

## API接口

### 车辆相关API
- `GET /api/cars/` - 获取车辆列表
- `GET /api/cars/{id}/` - 获取车辆详情
- `POST /api/cars/{id}/favorite/` - 收藏/取消收藏车辆

### 用户相关API
- `GET /api/users/profile/` - 获取用户资料
- `PUT /api/users/profile/` - 更新用户资料
- `GET /api/users/favorites/` - 获取收藏列表

### AI推荐API
- `POST /api/ai/recommendations/` - 获取AI推荐
- `GET /api/ai/price-prediction/{car_id}/` - 价格预测

## 管理后台

管理后台提供完整的数据管理功能：
- 用户管理
- 车辆审核
- 交易监控
- 系统配置

访问 `/admin` 使用超级用户账号登录。

## 部署说明

### 生产环境部署

1. 设置 `DEBUG=False`
2. 配置生产数据库（PostgreSQL推荐）
3. 配置静态文件服务
4. 设置域名和HTTPS
5. 配置WSGI服务器（Gunicorn + Nginx）

### Docker部署

```dockerfile
# Dockerfile示例
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "used_car_system.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 开发团队

- 项目经理：负责项目规划和进度管理
- 后端开发：Django框架开发和API设计
- 前端开发：界面设计和用户体验优化
- AI工程师：机器学习算法开发和优化

## 许可证

本项目采用MIT许可证。

## 联系方式

如有问题或建议，请联系：
- 邮箱：support@usedcar.com
- 电话：400-123-4567