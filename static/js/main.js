// 二手车交易平台主JavaScript文件

// 全局变量和配置
const CONFIG = {
    API_BASE_URL: '/api/',
    CSRF_TOKEN: getCookie('csrftoken'),
    DEBUG: true
};

// 工具函数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(message, type = 'info') {
    // 创建Toast元素
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // 添加到页面
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    toastContainer.appendChild(toast);
    
    // 显示Toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // 自动移除
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// API调用函数
async function apiCall(endpoint, options = {}) {
    const url = CONFIG.API_BASE_URL + endpoint;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CONFIG.CSRF_TOKEN
        }
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, config);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API调用失败:', error);
        showToast('网络请求失败，请稍后重试', 'danger');
        throw error;
    }
}

// 车辆相关功能
class CarManager {
    static async getCars(filters = {}) {
        const params = new URLSearchParams(filters);
        return await apiCall(`cars/?${params}`);
    }
    
    static async getCarDetail(carId) {
        return await apiCall(`cars/${carId}/`);
    }
    
    static async toggleFavorite(carId) {
        return await apiCall(`cars/${carId}/favorite/`, {
            method: 'POST'
        });
    }
    
    static async searchCars(query) {
        return await apiCall(`cars/search/?q=${encodeURIComponent(query)}`);
    }
}

// 用户相关功能
class UserManager {
    static async getProfile() {
        return await apiCall('users/profile/');
    }
    
    static async updateProfile(data) {
        return await apiCall('users/profile/', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    static async getFavorites() {
        return await apiCall('users/favorites/');
    }
}

// AI推荐功能
class AIRecommender {
    static async getRecommendations(preferences = {}) {
        return await apiCall('ai/recommendations/', {
            method: 'POST',
            body: JSON.stringify(preferences)
        });
    }
    
    static async getPricePrediction(carId) {
        return await apiCall(`ai/price-prediction/${carId}/`);
    }
}

// 聊天功能
class ChatManager {
    static async getChatRooms() {
        return await apiCall('chat/rooms/');
    }
    
    static async getMessages(roomId) {
        return await apiCall(`chat/rooms/${roomId}/messages/`);
    }
    
    static async sendMessage(roomId, content) {
        return await apiCall(`chat/rooms/${roomId}/messages/`, {
            method: 'POST',
            body: JSON.stringify({ content })
        });
    }
}

// 图片上传功能
class ImageUploader {
    static async uploadImage(file, type = 'car') {
        const formData = new FormData();
        formData.append('image', file);
        formData.append('type', type);
        
        return await apiCall('upload/image/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': CONFIG.CSRF_TOKEN
            },
            body: formData
        });
    }
    
    static previewImage(input, previewId) {
        const preview = document.getElementById(previewId);
        const file = input.files[0];
        
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    }
}

// 表单验证
class FormValidator {
    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }
    
    static validatePhone(phone) {
        const re = /^1[3-9]\d{9}$/;
        return re.test(phone);
    }
    
    static validatePassword(password) {
        return password.length >= 6;
    }
    
    static validateForm(form) {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.markInvalid(input, '此字段为必填项');
                isValid = false;
            } else {
                this.markValid(input);
            }
        });
        
        return isValid;
    }
    
    static markInvalid(input, message) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        
        let feedback = input.nextElementSibling;
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            input.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    }
    
    static markValid(input) {
        input.classList.add('is-valid');
        input.classList.remove('is-invalid');
    }
}

// 页面初始化函数
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 初始化弹出框
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // 自动隐藏消息提示
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // 初始化图片预览
    const imageInputs = document.querySelectorAll('input[type="file"][data-preview]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const previewId = this.getAttribute('data-preview');
            ImageUploader.previewImage(this, previewId);
        });
    });
    
    // 表单提交处理
    const forms = document.querySelectorAll('form[data-ajax]');
    forms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!FormValidator.validateForm(this)) {
                return;
            }
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // 显示加载状态
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> 处理中...';
            
            try {
                const formData = new FormData(this);
                const response = await fetch(this.action, {
                    method: this.method,
                    body: formData,
                    headers: {
                        'X-CSRFToken': CONFIG.CSRF_TOKEN
                    }
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    showToast(result.message || '操作成功', 'success');
                    
                    // 如果有重定向URL，则跳转
                    if (result.redirect_url) {
                        setTimeout(() => {
                            window.location.href = result.redirect_url;
                        }, 1000);
                    }
                } else {
                    showToast(result.message || '操作失败', 'danger');
                }
            } catch (error) {
                console.error('表单提交失败:', error);
                showToast('网络错误，请稍后重试', 'danger');
            } finally {
                // 恢复按钮状态
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        });
    });
});

// 导出到全局作用域
window.CarManager = CarManager;
window.UserManager = UserManager;
window.AIRecommender = AIRecommender;
window.ChatManager = ChatManager;
window.ImageUploader = ImageUploader;
window.FormValidator = FormValidator;
window.showToast = showToast;