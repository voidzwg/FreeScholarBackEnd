from .utils import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from user.models import *
from django_redis import get_redis_connection
import simplejson as simplejson
from django.core import serializers
from django.core.serializers import json
from django.shortcuts import render
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import User, Scholar, Follow, Comment, Like1
import simplejson as simplejson
from django.core import serializers
from django.core.serializers import json
from django.shortcuts import render

# publish/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import User, Scholar, Follow, Comment, Like1

SUPERUSER = [6]

token_expire = 60 * 60 * 1
r = get_redis_connection()


@csrf_exempt  # 跨域设置
def register(request):  # 继承请求类
    if request.method != 'POST':
        return JsonResponse({'result': 0, 'msg': "请求方式错误"})
    # 判断请求方式是否为 POST
    try:
        data_body = request.POST

        username = data_body.get('username')  # 获取请求体中的请求数据
        email = data_body.get('email')
        password_1 = data_body.get('password1')
        password_2 = data_body.get('password2')

        new_user = User()
        if len(username) > 10:
            return JsonResponse({'result': 0, 'msg': "用户名过长"})

        new_user.name = username

        if not new_user.validate_username():
            JsonResponse({'result': 0, 'msg': "用户名含有非法字符"})

        if User.objects.filter(name=username).exists():
            return JsonResponse({'result': 0, 'msg': "用户名已被使用"})

        new_user.mail = email
        print(email)
        if not new_user.validate_email():
            return JsonResponse({'result': 0, 'msg': "邮箱不合法"})
        # if User.objects.filter(mail=email).exists():
        #     return JsonResponse({'result': 0, 'msg': "邮箱已被使用"})

        if len(password_1) < 5 or len(password_1) > 18:
            return JsonResponse({'result':
                                     0, 'msg': "密码长度不合法"})

        if password_1 != password_2:
            return JsonResponse({'result': 0, 'msg': "两次输入的密码不同"})

        new_user.pwd = password_1

        if not new_user.validate_password():
            return JsonResponse({'result': 0, 'msg': "密码类型不合法"})

            # 新建 Author 对象，赋值用户名和密码保存

        # id 是自动复制，不需要指明
        new_user.save()
        return JsonResponse({'result': 1, 'msg': "注册成功"})
    except Exception as e:
        traceback.print_exc()


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'result': 1, 'msg': "请求方式错误"})

    # if request.session.get('username', 0) != 0:
    #     return JsonResponse({'result': 1, 'msg': "用户已登录"})
    try:
        data_body = request.POST

        username = data_body.get('username')
        password = data_body.get('password')

        if User.objects.filter(name=username).exists():
            # 用 filter 检查其存在性
            user = User.objects.get(name=username)
        else:
            return JsonResponse({'result': 1, 'msg': "用户不存在"})

        if user.pwd == password:
            # request.session['username'] = user.username
            token = Token.create_token(username, password)
            gettoekn = Token.check_token(token)
            r.set(username, token, token_expire)
            userInfo = {
                'errno': 0,
                'id': user.field_id,
                'name': user.name,
                'password': user.pwd,
                'email': user.mail,
                'profile': user.bio,
                'avator': user.avatar,
                'token': token,
                'getToken':gettoekn
            }
            return JsonResponse(userInfo)
        else:
            return JsonResponse({'result': 1, 'msg': "密码错误"})
    except Exception as e:
        traceback.print_exc()


# @csrf_exempt
def logout(request):
    try :
        if request.method != 'POST':
            return JsonResponse({'result': 1, 'msg': "请求方式错误"})
        token = request.POST.get("token")
        getToken1 = Token.check_token(token)
        username = getToken1.get("id")
        if r.get(username) is None:
            return JsonResponse({'result': 1, 'msg': "请先登录"})
        Token2 = r.get(username).decode()
        if token == Token2:
            r.delete(username)
            return JsonResponse({'result': 0, 'msg': "注销成功"})
        else:
            return JsonResponse({'result': 1, 'msg': "token错误"})
    except Exception as e:
        traceback.print_exc()


@csrf_exempt
def test(request):
    if request.method == 'GET':
        user_id = request.GET.get("id", None)
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        return JsonResponse({'errno': 0, 'id': user_id, 'name': user.name})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getBaseInfo(request):
    # if request.method == 'GET':
    #     user_id = request.GET['user_id']  # 获取请求数据
    if request.method != 'POST':
        return JsonResponse({'result': 1, 'msg': "请求方式错误"})
    token = request.POST.get("token")
    getToken1 = Token.check_token(token)
    username = getToken1.get("id")
    if r.get(username) is None:
        return JsonResponse({'result': 1, 'msg': "请先登录"})
    Token2 = r.get(username).decode()
    if token == Token2:
        counts = 0
        try:
            user = User.objects.get(name=username)
            user_id=user.field_id
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        bio = user.bio
        u_name = user.name
        try:
            scholar = Scholar.objects.get(user_id=user_id)
        except Scholar.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "该用户不是学者"})
        affi = scholar.affi
        try:
            user_count = len(Follow.objects.filter(user_id=user_id))
        except Follow.DoesNotExist:
            user_count = 0
        try:
            scholar_count = len(Follow.objects.filter(scholar_id=user_id))
        except Follow.DoesNotExist:
            scholar_count = 0
        try:
            likes = Comment.objects.filter(user_id=user_id)
        except Comment.DoesNotExist:
            counts = 0
            likes = None
        for i in range(len(likes)):
            c_id = likes[i]._id
            try:
                counts += len(Like1.objects.filter(user_id=c_id))
            except Like1.DoesNotExist:
                counts += 0
        return JsonResponse({'username': u_name, 'institution': affi, 'bio': bio, 'follows': user_count
                                , 'followers': scholar_count, 'likes': counts})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getFollows(request):
    # if request.method == 'GET':
    #     user_id = request.GET['user_id']  # 获取请求数据
    if request.method != 'POST':
        return JsonResponse({'result': 1, 'msg': "请求方式错误"})
    token = request.POST.get("token")
    getToken1 = Token.check_token(token)
    username = getToken1.get("id")
    if r.get(username) is None:
        return JsonResponse({'result': 1, 'msg': "请先登录"})
    Token2 = r.get(username).decode()
    if token == Token2:
        user=User.objects.get(name=username)
        user_id=user.field_id
        data = []
        try:
            users = Follow.objects.filter(user_id=user_id)
        except Follow.DoesNotExist:
            return JsonResponse(data)
        for i in range(len(users)):
            scholar_id = users[i].scholar_id
            try:
                scholar = Scholar.objects.get(field_id=scholar_id)
            except Scholar.DoesNotExist:
                continue
            user_id = scholar.user_id
            affi = scholar.affi
            try:
                user = User.objects.get(field_id=user_id)
            except User.DoesNotExist:
                continue
            bio = user.bio
            u_name = user.name
            data1 = {'id': user_id, 'institution': affi, 'username': u_name, 'bio': bio,
                     'time': users[i].create_time}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getFollowers(request):
    # if request.method == 'GET':
    #     user_id = request.GET['user_id']  # 获取请求数据
    if request.method != 'POST':
        return JsonResponse({'result': 1, 'msg': "请求方式错误"})
    token = request.POST.get("token")
    getToken1 = Token.check_token(token)
    username = getToken1.get("id")
    if r.get(username) is None:
        return JsonResponse({'result': 1, 'msg': "请先登录"})
    Token2 = r.get(username).decode()
    if token == Token2:
        user=User.objects.get(name=username)
        user_id=user.field_id
        data = []
        try:
            users = Follow.objects.filter(scholar_id=user_id)
        except Follow.DoesNotExist:
            return JsonResponse(data)
        for i in range(len(users)):
            user_id = users[i].user_id
            try:
                user = User.objects.get(field_id=user_id)
            except User.DoesNotExist:
                continue
            bio = user.bio
            u_name = user.name
            data1 = {'id': user_id, 'username': u_name, 'bio': bio,
                     'time': users[i].create_time}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})



