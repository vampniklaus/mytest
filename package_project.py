#!/usr/bin/env python3
"""
项目打包脚本
用于将Django项目打包成可部署的格式
"""

import os
import shutil
import zipfile
from pathlib import Path
import sys

def create_project_package():
    """创建项目打包文件"""
    
    # 项目根目录
    project_root = Path(__file__).parent
    package_name = "used_car_system_package"
    package_dir = project_root / package_name
    
    # 需要包含的文件和目录
    include_patterns = [
        "manage.py",
        "requirements.txt",
        "create_test_data.py",
        "README.md",
        ".env.example",
        "used_car_system/",
        "users/",
        "cars/",
        "transactions/",
        "chat/",
        "ai_recommendation/",
        "templates/",
        "static/",
    ]
    
    # 需要排除的文件和目录
    exclude_patterns = [
        "__pycache__",
        "*.pyc",
        "db.sqlite3",
        ".git",
        ".vscode",
        ".idea",
    ]
    
    print("开始打包项目...")
    
    # 创建打包目录
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # 复制文件
    for pattern in include_patterns:
        source_path = project_root / pattern
        
        if source_path.is_file():
            # 复制单个文件
            dest_path = package_dir / pattern
            shutil.copy2(source_path, dest_path)
            print(f"复制文件: {pattern}")
        elif source_path.is_dir():
            # 复制目录
            dest_dir = package_dir / pattern
            shutil.copytree(source_path, dest_dir, 
                          ignore=shutil.ignore_patterns(*exclude_patterns))
            print(f"复制目录: {pattern}")
    
    # 创建部署说明文件
    create_deployment_guide(package_dir)
    
    # 创建ZIP包
    zip_filename = f"{package_name}.zip"
    zip_path = project_root / zip_filename
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    # 清理临时目录
    shutil.rmtree(package_dir)
    
    print(f"\n打包完成！")
    print(f"打包文件: {zip_path}")
    print(f"文件大小: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
    
    return zip_path

def create_deployment_guide(package_dir):
    """创建部署指南"""
    
    guide_content = """# 二手车交易系统 - 部署指南

## 系统要求
- Python 3.8+
- Django 4.2.7
- 数据库: SQLite (开发环境) / PostgreSQL (生产环境)

## 快速部署

### 1. 环境准备
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境配置
```bash
# 复制环境变量文件
cp .env.example .env

# 编辑 .env 文件，设置 SECRET_KEY 等配置
```

### 3. 数据库初始化
```bash
# 迁移数据库
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 可选：导入测试数据
python create_test_data.py
```

### 4. 启动服务
```bash
# 开发环境
python manage.py runserver

# 生产环境 (使用Gunicorn)
gunicorn used_car_system.wsgi:application
```

## 项目结构
```
used_car_system_package/
├── manage.py              # Django管理脚本
├── requirements.txt       # 依赖包列表
├── README.md             # 项目说明
├── .env.example          # 环境变量示例
├── used_car_system/      # 项目配置
├── users/                # 用户管理应用
├── cars/                 # 车辆管理应用
├── transactions/         # 交易管理应用
├── chat/                 # 聊天功能应用
├── ai_recommendation/    # AI推荐应用
├── templates/            # 模板文件
└── static/              # 静态文件
```

## 主要功能
- 用户注册/登录/认证
- 车辆信息管理
- 交易流程管理
- 实时聊天功能
- AI智能推荐

## 注意事项
- 生产环境请设置 DEBUG=False
- 配置合适的 ALLOWED_HOSTS
- 使用安全的SECRET_KEY
- 定期备份数据库
"""
    
    with open(package_dir / "DEPLOYMENT_GUIDE.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)

def create_docker_config():
    """创建Docker部署配置"""
    
    dockerfile_content = """# Dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建静态文件目录
RUN mkdir -p staticfiles

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["gunicorn", "used_car_system.wsgi:application", "--bind", "0.0.0.0:8000"]
"""
    
    docker_compose_content = """# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-production-secret-key
    volumes:
      - ./data:/app/data
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
"""
    
    project_root = Path(__file__).parent
    
    with open(project_root / "Dockerfile", 'w') as f:
        f.write(dockerfile_content)
    
    with open(project_root / "docker-compose.yml", 'w') as f:
        f.write(docker_compose_content)
    
    print("Docker配置文件已创建")

if __name__ == "__main__":
    try:
        # 创建主打包
        zip_file = create_project_package()
        
        # 创建Docker配置
        create_docker_config()
        
        print("\n打包完成！项目已准备好部署。")
        print("\n下一步：")
        print("1. 使用 package_project.py 创建的ZIP包进行分发")
        print("2. 参考 DEPLOYMENT_GUIDE.md 进行部署")
        print("3. 使用Docker配置进行容器化部署")
        
    except Exception as e:
        print(f"打包过程中出现错误: {e}")
        sys.exit(1)