from django.shortcuts import render, redirect,get_object_or_404
from Login.models import *
from django.http import JsonResponse
from  Char.models import *
from  Login.forms import *
from  Goodshow.models import *
from Login.views import isLogin
from django.db.models import Sum
# Create your views here.
@isLogin
def char(request):
    id = request.session.get('user_id')
    goods=CartInfo.objects.filter(user__id=id)
    list1=[]
    try:
        for good in goods:
            buy=GoodsInfo.objects.get(id=good.goods_id)
            count=good.count
            list1.append({'buy':buy,'count':count,'good':good})
            c = CartInfo.objects.filter(user_id=id).aggregate(Sum('count'))
            request.session['cart_count'] = c
        return render(request,'Char/cart.html',{'title': '购物车','list1':list1,'good':good,'c':c})
    except :
        return render(request,'Char/cart.html')
@isLogin
def add_char(request):
    user = request.session.get('user_id')
    dict1 = request.GET
    gid = dict1.get('gid')  # 商品ID
    count = int(dict1.get('count', 0))  # 数量

    a=CartInfo.objects.filter(goods_id=gid,user_id=user)
    if a:
        a=a[0]
        a.count += count
        a.save()

    else:


        order=CartInfo()
        order.goods=GoodsInfo.objects.get(id=gid)
        order.count=count
        order.user=User.objects.get(id=user)
        order.save()
    c = CartInfo.objects.filter(user_id=user).aggregate(Sum('count'))
    # 购物车商品数量
    request.session['cart_count'] = c
    return JsonResponse({'ok': 1, 'count': c.get('count__sum')})

@isLogin
def removechar(request):
    user = request.session.get('user_id')
    cid = request.GET.get('cid')
    oeder=CartInfo.objects.get(id=cid)
    oeder.delete()
    c = CartInfo.objects.filter(user_id=user).aggregate(Sum('count'))
    # 购物车商品数量
    request.session['cart_count'] = c
    return JsonResponse({'ok': 1})


def edit(request):
    dict = request.GET
    count = int(dict.get('count'))
    cid = dict.get('cid')

    cart = get_object_or_404(CartInfo, id=cid)
    cart.count = count
    cart.save()
    return JsonResponse({'ok': 1})