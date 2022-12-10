import traceback

# publish/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from user.models import User, Scholar, Follow
from utils.Token import Authentication
from utils.media import *

token_expire = 60 * 60 * 1
r = get_redis_connection()


@csrf_exempt  # 跨域设置
def register(request):  # 继承请求类
    if request.method != 'POST':
        return JsonResponse({'errno': 0, 'msg': "请求方式错误"})
    # 判断请求方式是否为 POST
    try:
        data_body = request.POST
        username = data_body.get('username')  # 获取请求体中的请求数据
        email = data_body.get('email')
        password_1 = data_body.get('password1')
        password_2 = data_body.get('password2')

        new_user = User()
        if len(username) > 10:
            return JsonResponse({'errno': 0, 'msg': "用户名过长"})

        new_user.name = username

        if not new_user.validate_username():
            JsonResponse({'errno': 0, 'msg': "用户名含有非法字符"})

        if User.objects.filter(name=username).exists():
            return JsonResponse({'errno': 0, 'msg': "用户名已被使用"})

        new_user.mail = email
        print(email)
        if not new_user.validate_email():
            return JsonResponse({'errno': 0, 'msg': "邮箱不合法"})
        # if User.objects.filter(mail=email).exists():
        #     return JsonResponse({'errno': 0, 'msg': "邮箱已被使用"})

        if len(password_1) < 5 or len(password_1) > 18:
            return JsonResponse({'errno':
                                     0, 'msg': "密码长度不合法"})

        if password_1 != password_2:
            return JsonResponse({'errno': 0, 'msg': "两次输入的密码不同"})

        new_user.pwd = password_1

        if not new_user.validate_password():
            return JsonResponse({'errno': 0, 'msg': "密码类型不合法"})

            # 新建 Author 对象，赋值用户名和密码保存

        # id 是自动复制，不需要指明
        # 设置头像为默认头像
        new_user.avatar = DEFAULT_AVATAR
        new_user.save()
        return JsonResponse({'errno': 1, 'msg': "注册成功"})
    except Exception as e:
        traceback.print_exc()


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(name=username)
    except User.DoesNotExist:
        return JsonResponse({'errno': 1, 'msg': "用户不存在"})

    if user.pwd == password:
        token = Authentication.create_token(user.field_id)
        user_info = {
            'errno': 0,
            'name': user.name,
            'email': user.mail,
            'profile': user.bio,
            'avatar': user.avatar,
            'token': token,
        }
        return JsonResponse(user_info)
    else:
        return JsonResponse({'errno': 1, 'msg': "密码错误"})


@csrf_exempt
def logout(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    Authentication.logout(payload.get('id'))
    return JsonResponse({'errno': 0, 'msg': "注销成功"})


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
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    # counts = 0
    try:
        user_id = payload.get('id')
        user = User.objects.get(field_id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'errno': 1, 'msg': "用户不存在"})
    bio = user.bio
    avatar=user.avatar
    u_name = user.name
    try:
        user_count = len(Follow.objects.filter(user_id=user_id))
    except Follow.DoesNotExist:
        user_count = 0
    try:
        scholar = Scholar.objects.get(user_id=user_id)
    except Scholar.DoesNotExist:
        return JsonResponse(
            {'username': u_name, 'avator': avatar, 'institution': None, 'bio': bio, 'follows': user_count
                , 'followers': 0})
    affi = scholar.affi
    try:
        scholar_count = len(Follow.objects.filter(scholar_id=user_id))  # FIXME
    except Follow.DoesNotExist:
        scholar_count = 0
    # try:
    #     likes = Comment.objects.filter(user_id=user_id)  # FIXME: 可以和ysa交流一下，用户似乎是没有获赞数的
    # except Comment.DoesNotExist:
    #     counts = 0
    #     likes = None
    # for like in likes:  # FIXME: 额外开销，可以直接 for like in likes，Comment表里存了点赞数据
    #     c_id = like._id
    #     try:
    #         counts += len(Like1.objects.filter(user_id=c_id))
    #     except Like1.DoesNotExist:
    #         counts += 0
    return JsonResponse({'username': u_name, 'avator':avatar,'institution': affi, 'bio': bio, 'follows': user_count
                            , 'followers': scholar_count})  # FIXME: avatar


@csrf_exempt
def getFollows(request):
    # if request.method == 'GET':
    #     user_id = request.GET['user_id']  # 获取请求数据
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    user_id = payload.get('id')
    user = User.objects.get(field_id=user_id)
    data = []
    try:
        users = Follow.objects.filter(user_id=user_id)
    except Follow.DoesNotExist:
        return JsonResponse(data)
    for user in users:  # FIXME: for user in users
        scholar_id = user.scholar.scholar_id  # FIXME: scholar_id = user.scholar.field_id
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
                 'time': user.create_time}
        data.append(data1)
    return JsonResponse(data, safe=False)


@csrf_exempt
def getFollowers(request):
    # if request.method == 'GET':
    #     user_id = request.GET['user_id']  # 获取请求数据
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    user = User.objects.get(field_id=payload.get('id'))
    user_id = user.field_id  # FIXME: payload中已经有uid了
    data = []
    try:
        users = Follow.objects.filter(scholar_id=user_id)
    except Follow.DoesNotExist:
        return JsonResponse(data)
    for i in range(len(users)):  # FIXME: for user in users
        user_id = users[i].user_id  # FIXME: user_id = user.user.field_id
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
