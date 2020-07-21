from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from Goodshow.models import *
# Create your views here.
def index(request):
    type_list = TypeInfo.objects.all()  # 查询所有分类
    list1 = []
    for type_info in type_list:
        new = type_info.goodsinfo_set.order_by('-id')[0:4]
        fire = type_info.goodsinfo_set.order_by('-gclick')[0:3]
        list1.append({'type': type_info, 'new': new, 'fire': fire})

    context = {'title': '首页', 'isGoods': 1, 'list1': list1}
    return render(request, 'Goodshow/index.html', context)


def goods_list(request, tid, page_num, ord_str):
    types = TypeInfo.objects.all()  # 查找到所有分类
    type_cur = get_object_or_404(TypeInfo, id=tid)  # 当前分类
    gnew = type_cur.goodsinfo_set.order_by('-id')[0:2]  # 新品推荐

    # 排序方式
    order = '-id'
    if ord_str == '1':
        order = '-gprice'
    elif ord_str == '2':
        order = '-gclick'

    # 按条件查找商品
    glist = type_cur.goodsinfo_set.order_by(order)
    p = Paginator(glist, 10)
    page = p.page(int(page_num))

    context = {
        'title': '商品列表',
        'isGoods': 1,
        'page': page,
        'types': types,
        'tid': tid,
        'type': type_cur,
        'ord_str': ord_str,
        'gnew': gnew,
    }
    return render(request, 'Goodshow/list.html', context)

def goods_detail(request, id):
    g = get_object_or_404(GoodsInfo, id=id)
    g.gclick += 1
    g.save()
    gnew = g.gtype.goodsinfo_set.order_by('-id')[0:2]

    context = {'title': '商品详情', 'isGoods': 1, 'gnew': gnew, 'g': g}
    res= render(request, 'Goodshow/detail.html', context)
    jin = request.COOKIES.get('jin', '[]')
    jin_list = eval(jin)
    if jin:
        if id in jin_list:
            jin_list.remove(id)
        jin_list.insert(0, id)
        if len(jin_list) > 5:
            jin_list.pop()
    res.set_cookie('jin', str(jin_list))
    return res