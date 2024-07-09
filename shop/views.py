from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from .forms import LoginForm
# from .models import User
# from django.contrib.auth.models import User
from .models import Goods, GoodsType
from django.contrib.auth.forms import UserCreationForm

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('/')  # 注册成功后重定向到首页或其他页面
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('/')  # 登录成功后重定向到首页或其他页面
#             else:
#                 form.add_error(None, '无效的用户名或密码')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

def index_views(request):
    products = Goods.objects.filter(isActive=True).order_by('-id')[:3]
    context = {
        'products': products
    }
    return render(request, 'index.html', context)

def shop_views(request):
    categories = GoodsType.objects.all()
    products = Goods.objects.filter(isActive=True)

    # 处理类别筛选
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(goodsType_id=category_id)

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'shop.html', context)

def product_detail_views(request, product_id):
    product = get_object_or_404(Goods, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'detail.html', context)

# def check_login_views(request):
#     if request.user.is_authenticated:
#         login_status = 1
#         uname = request.user.uname
#         dic = {
#             'loginStatus': login_status,
#             'uname': uname
#         }
#     else:
#         dic = {'loginStatus': 0}
#     return JsonResponse(dic)

# def logout_view(request):
#     logout(request)
#     return redirect('/')

# def logout_cart_views(request):
#     if 'uid' in request.session and 'uphone' in request.session:
#         del request.session['uid']
#         del request.session['uphone']
#         resp = HttpResponseRedirect('/')
#         if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
#             resp.delete_cookie('uid')
#             resp.delete_cookie('uphone')
#             return resp
#     return redirect('/')

# def type_goods_views(request):
#     all_list = []
#     types = GoodsType.objects.all()
#     for type in types:
#         type_json = type.to_dict()
#         g_list = type.goods_set.filter(isActive=True).order_by("-id")[:10]
#         g_list_json = serializers.serialize('json', g_list)
#         dic = {
#             "type": type_json,
#             "goods": g_list_json,
#         }
#         all_list.append(dic)
#     return JsonResponse(all_list, safe=False)
#     #return HttpResponse(json.dumps({"data": all_list}), content_type='application/json')



# @login_required
def add_cart_views(request):
    good_id = request.GET['gid']
    user_id = request.user.id
    ccount = 1
    cart_list = CartInfo.objects.filter(user_id=user_id, goods_id=good_id)
    if cart_list.exists():
        cartinfo = cart_list.first()
        cartinfo.ccount += ccount
        cartinfo.save()
        status_text = '更新数量成功'
    else:
        CartInfo.objects.create(user_id=user_id, goods_id=good_id, ccount=ccount)
        status_text = '添加購物車成功'
    return JsonResponse({'status': 1, 'statusText': status_text})

# @login_required
def cart_views(request):
    return render(request, 'cart.html')

def goods_cart_view(request):
    all_list = []
    user_id = request.session['uid']
    carts = CartInfo.objects.filter(user_id=user_id).all()

    for c in carts:
        c_dump = json.dumps(c.to_dict())
        g = Goods.objects.filter(id=c.goods.id).all()
        g_list_json = serializers.serialize('json', g)
        dic = {
            "data": c_dump,
            "p":g_list_json
        }
        all_list.append(dic)

    return HttpResponse(json.dumps(all_list))
    #return HttpResponse(json.dumps({"data": all_list}), content_type='application/json')

# @login_required
def delete_cart(request):
    good_id = request.GET['gid']
    user_id = request.user.id
    cart_list = CartInfo.objects.filter(user_id=user_id, goods_id=good_id)
    if cart_list.exists():
        cart_list.first().delete()
        status_text = '刪除購物車成功'
    else:
        status_text = '狀態異常'
    return JsonResponse({'status': 1, 'statusText': status_text})