from django.shortcuts import render, redirect,get_object_or_404
from Login.models import *
from django.http import JsonResponse
from  Goodshow.models import *
from  Login.forms import *
# Create your views here.
from OrderDetail.models import *
def isLogin(func):
    def inner(request, *args, **kwargs):
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return JsonResponse({'isNotLogin': 1})
            return redirect('login')

    return inner

def register(request):
    return render(request, 'User/register.html', {'title': '注册'})


def login(request):
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')#获得上一次的页面地址
    return render(request, 'User/login.html', {'title': '登录'})


def user_check(request):
    uname = request.GET.get('uname')
    count = User.objects.filter(uname=uname).count()
    return JsonResponse({'num': count})


from hashlib import sha1


def register_check(request):
    post = request.POST
    uname = post.get('user_name')
    if not uname:
        return redirect('register')
    upwd = post.get('pwd')
    cpwd = post.get('cpwd')
    uemail = post.get('email')
    if upwd != cpwd:
        return redirect('register')
    s1 = sha1()#加密
    s1.update(upwd.encode())
    upwd = s1.hexdigest()
    user = User()
    user.uname = uname
    user.upwd = upwd
    user.uemail = uemail
    user.save()
    return redirect('login')


def login_check(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = User.objects.filter(uname=uname)
    if users:
        s1 = sha1()
        s1.update(upwd.encode())
        if s1.hexdigest() == users[0].upwd:
            # res = redirect(request.session.get('login_from'))
            res = redirect('/')

            if jizhu:
                res.set_cookie('uname', uname)
            else:
                res.set_cookie('uname', '', max_age=-1)#到浏览器关闭之前
            request.session['user_name'] = uname
            request.session['user_id'] = users[0].id
            return res
    content = {'title': '登录', 'error_msg': 1, 'uname': uname}
    return render(request, 'User/login.html', content)

def logout(request):
    request.session.flush()
    return redirect('/')


@isLogin
def info(request):
    id = request.session.get('user_id')
    user1 = UserAddressInfo.objects.filter(user__id=id)
    if user1:
        user1=user1[0]
    jin = request.COOKIES.get('jin', '[]')
    jin_list = eval(jin)
    goods = [GoodsInfo.objects.get(pk=id) for id in jin_list]
    return render(request, 'User/user_center_info.html', {'title': '个人信息', 'user1': user1, 'goods': goods})

@isLogin
def user_order(request):
    id = request.session.get('user_id')
    orders=OrderInfo.objects.filter(user_id=id)
    if orders:
        list1=[]
        for order in orders:
            orderDetil=OrderDetailInfo.objects.filter(order=order.oid)

            list1.append({'order':order,'orderDetil':orderDetil,})
    print(list1)
    return render(request, 'User/user_center_order.html', {'title': '全部订单','list1':list1})


@isLogin
def user_site(request):
    id = request.session.get('user_id')
    user1 = UserAddressInfo.objects.filter(user__id=id)
    if user1:
        user1=user1[0]
        str1 = f'{user1.uaddress} ({user1.uname}收) {user1.uphone}'
    else:
        str1 ="请输入收货地址"
    form = UserForm()
    return render(request, 'User/user_center_site.html', {'title': '收货地址', 'str': str1, 'form': form})


@isLogin
def user_save(request):
    id = request.session.get("user_id")

    user1 = UserAddressInfo.objects.filter(user=id)
    if user1:
        user1=user1[0]
        form = UserForm(request.POST, instance=user1)
    else:
        user=UserAddressInfo()
        user.user=User.objects.get(id=id)
        form = UserForm(request.POST, instance=user)
    if form.is_valid():
        form.save()
    return redirect('site')
