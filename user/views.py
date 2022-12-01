from .utils import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from user.models import *
from django_redis import get_redis_connection

# token_expire = 60*60*1
# r = get_redis_connection()

@csrf_exempt  # 跨域设置
def register(request):  # 继承请求类
    if request.method != 'POST':
        return JsonResponse({'result': 0, 'msg': "请求方式错误"})
    # 判断请求方式是否为 POST

    try:
        data_body = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        data_body = request.POST

    username = data_body.get('username')  # 获取请求体中的请求数据
    email = data_body.get('email')
    password_1 = data_body.get('password1')
    password_2 = data_body.get('password2')

    new_user = User()

    if len(username) > 10:
        return JsonResponse({'result': 0, 'msg': "用户名过长"})

    new_user.username = username

    if not new_user.validate_username():
        JsonResponse({'result': 0, 'msg': "用户名含有非法字符"})

    if User.objects.filter(username=username).exists():
        return JsonResponse({'result': 0, 'msg': "用户名已被使用"})

    new_user.email = email
    if not new_user.validate_email():
        return JsonResponse({'result': 0, 'msg': "邮箱不合法"})
    if User.objects.filter(email=email).exists():
        return JsonResponse({'result': 0, 'msg': "邮箱已被使用"})

    if len(password_1) < 5 or len(password_1) > 18:
        return JsonResponse({'result': 0, 'msg': "密码长度不合法"})

    if password_1 != password_2:
        return JsonResponse({'result': 0, 'msg': "两次输入的密码不同"})

    new_user.password = password_1

    if not new_user.validate_password():
        return JsonResponse({'result': 0, 'msg': "密码类型不合法"})

        # 新建 Author 对象，赋值用户名和密码保存

    # id 是自动复制，不需要指明
    new_user.save()
    return JsonResponse({'result': 1, 'msg': "注册成功"})


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'result': 1, 'msg': "请求方式错误"})

    if request.session.get('username', 0) != 0:
        return JsonResponse({'result': 1, 'msg': "用户已登录"})

    try:
        data_body = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        data_body = request.POST

    username = data_body.get('username')
    password = data_body.get('password')

    if User.objects.filter(name=username).exists():
        # 用 filter 检查其存在性
        user = User.objects.get(name=username)
    else:
        return JsonResponse({'result': 1, 'msg': "用户不存在"})

    if user.password == password:
        request.session['username'] = user.username
        # token = Token.create_token(username, password)
        # r.set(username, token, token_expire)
        userInfo = {
            'errno': 0,
            'id': user.field_id,
            'name': user.name,
            'password': user.pwd,
            'email': user.mail,
            'profile': user.bio,
            'avator': user.avatar,
            # 'token':token
        }
        return JsonResponse(userInfo)
    else:
        return JsonResponse({'result': 1, 'msg': "密码错误"})


@csrf_exempt
def logout(request):
    if request.method != 'POST':
        return JsonResponse({'result': 1, 'msg': "请求方式错误"})
    if request.session.get('username', 0) != 0:
        request.session.flush()
        return JsonResponse({'result': 0, 'msg': "注销成功"})
    else:
        return JsonResponse({'result': 1, 'msg': "请先登录"})
