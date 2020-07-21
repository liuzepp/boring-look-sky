from django.shortcuts import render, redirect,get_object_or_404
from Login.models import *
from django.http import JsonResponse
from  Char.models import *
from OrderDetail.models import *



# Create your views here.
def addorder(request):
    dict1 = request.GET
    cid = dict1.getlist('cid')
    print(cid)
    cart_list = CartInfo.objects.filter(id__in=cid)
    print(cart_list)
    uid = request.session.get('user_id')
    user = UserAddressInfo.objects.filter(id=uid)
    if user:
        user=user[0]
        str1 = f'{user.uaddress} ({user.uname}收) {user.uphone}'

    else:
        str1='请填写收货地址'
    content = {'title': '订单支付', 'info': str1, 'clist': cart_list}
    return render(request,'Order/place_order.html' , content)

import os
import time
from django.db import transaction
from alipay import AliPay
from django.conf import settings

alipay = AliPay(
    appid=settings.ALIPAY_APPID,
    app_notify_url=None,
    app_private_key_path=os.path.join(settings.STATICFILES_DIRS[0], 'app_private_key.pem'),
    alipay_public_key_path=os.path.join(settings.STATICFILES_DIRS[0], 'alipay_public_key.pem'),
    sign_type='RSA',
    debug=True,
)


@transaction.atomic
def do_order(request):
    pay_method = request.GET.get('pay_style')
    cid = request.GET.getlist('cid')

    print(pay_method)
    print(cid)
    uid = request.session.get('user_id')
    user = UserAddressInfo.objects.get(id=uid)

    # 开启事务
    sid = transaction.savepoint()
    # 创建订单
    order = OrderInfo()
    order.oid = str(int(time.time() * 1000)) + str(uid)
    order.user_id = uid
    order.ototal = 0
    order.oaddress = user.uaddress
    order.save()

    cart_list = CartInfo.objects.filter(id__in=cid)
    total = 0
    isOk = True

    for cart in cart_list:
        if cart.count <= cart.goods.gkucun:
            # 库存充足
            detail = OrderDetailInfo()
            detail.order = order
            detail.goods = cart.goods
            detail.price = cart.goods.gprice
            detail.count = cart.count
            detail.save()
            # 计算总价
            total += detail.count * detail.price
            # 更改库存
            cart.goods.gkucun -= cart.count
            # 删除购物车对象
            cart.delete()
        else:
            isOk = False
    if isOk:
        # 保存总价
        order.ototal = total
        order.save()
        # 货到付款
        if pay_method == 'cash':
            order.oisPay = 1
            order.save()
            transaction.savepoint_commit(sid)  # 提交事务
            return JsonResponse({'res': 1, 'message': 'OK'})
        else:

            order_id = order.oid
            print(order_id,'----------------------------!!!!!')
            total_pay = order.ototal
            # total_pay = pay
            try:
                order_string = alipay.api_alipay_trade_page_pay(
                    out_trade_no=order_id,
                    total_amount=str(total_pay),
                    subject=f'果然鲜{order_id}',
                    return_url='http://127.0.0.1:8000/check_pay/?order_id=' + order_id,
                    notify_url='http://127.0.0.1:8000/check_pay/?order_id=' + order_id,
                )
            except Exception as e:
                print(e)

            alipay_url = settings.ALIPAY_URL + '?' + order_string

            return JsonResponse({'res': 3, 'messege': 'OK', 'pay_url': alipay_url, 'order_id': order_id})
    else:
        transaction.savepoint_rollback(sid)
        return JsonResponse({'res': 0, 'message': 'Fail'})


def check_pay(request):
    order_id = request.GET.get('order_id')

    order = OrderInfo.objects.get(oid=order_id)
    while True:
        response = alipay.api_alipay_trade_query(order_id)

        code = response.get('code')
        trade_status = response.get('trade_status')
        if code == '10000' and trade_status == 'TRADE_SUCCESS':
            order.oisPay = 1
            order.save()
            return redirect('info')
        elif code == '40004' or (code == '10000' and trade_status == 'WAIT_BUYER_PAY'):
            continue
        else:
            return JsonResponse({'code': 0, 'message': '支付失败'})
