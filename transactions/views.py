from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction

@login_required
def transaction_list(request):
    """交易列表页面"""
    purchases = Transaction.objects.filter(buyer=request.user).select_related('car', 'seller')
    sales = Transaction.objects.filter(seller=request.user).select_related('car', 'buyer')
    
    return render(request, 'transactions/transaction_list.html', {
        'purchases': purchases,
        'sales': sales
    })

@login_required
def transaction_detail(request, transaction_id):
    """交易详情页面"""
    transaction = get_object_or_404(
        Transaction.objects.select_related('car', 'buyer', 'seller'), 
        id=transaction_id
    )
    
    # 检查权限
    if transaction.buyer != request.user and transaction.seller != request.user:
        return render(request, '403.html', status=403)
    
    return render(request, 'transactions/transaction_detail.html', {
        'transaction': transaction
    })