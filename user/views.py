import datetime
import traceback

# publish/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection

from user.models import *
from utils.Token import Authentication
from utils.media import *
from utils.superuser import ADMIN
from user.sendemail import *

token_expire = 60 * 60 * 1
r = get_redis_connection()


@csrf_exempt  # 跨域设置
def register(request):  # 继承请求类
    if request.method != 'POST':
        return JsonResponse({'errno': -1, 'msg': "请求方式错误"})
    # 判断请求方式是否为 POST
    try:
        data_body = request.POST
        username = data_body.get('username')  # 获取请求体中的请求数据
        email = data_body.get('email')
        password_1 = data_body.get('password1')
        password_2 = data_body.get('password2')

        new_user = User()
        if len(username) > 10:
            return JsonResponse({'errno': -2, 'msg': "用户名过长"})

        new_user.name = username

        if not new_user.validate_username():
            JsonResponse({'errno': 0, 'msg': "用户名含有非法字符"})

        if User.objects.filter(name=username).exists():
            return JsonResponse({'errno': -3, 'msg': "用户名已被使用"})

        new_user.mail = email
        print(email)
        if not new_user.validate_email():
            return JsonResponse({'errno': -4, 'msg': "邮箱不合法"})
        # if User.objects.filter(mail=email).exists():
        #     return JsonResponse({'errno': 0, 'msg': "邮箱已被使用"})

        if len(password_1) < 5 or len(password_1) > 18:
            return JsonResponse({'errno': -5, 'msg': "密码长度不合法"})

        if password_1 != password_2:
            return JsonResponse({'errno': -6, 'msg': "两次输入的密码不同"})

        new_user.pwd = password_1

        if not new_user.validate_password():
            return JsonResponse({'errno': -7, 'msg': "密码类型不合法"})

            # 新建 Author 对象，赋值用户名和密码保存

        # id 是自动复制，不需要指明
        # 设置头像为默认头像
        new_user.avatar = DEFAULT_AVATAR
        new_user.identity = 1
        new_user.state = 0
        new_user.gender = 0
        new_user.save()
        return JsonResponse({'errno': 0, 'msg': "注册成功"})
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

    if user.state == 2:
        return JsonResponse({'errno': 2, 'msg': "用户已被封禁"})

    if user.pwd == password:
        is_admin = (user.field_id in ADMIN)
        token = Authentication.create_token(user.field_id, admin=is_admin)
        user_info = {
            'errno': 0,
            'name': user.name,
            'email': user.mail,
            'profile': user.bio,
            'avatar': user.avatar,
            'token': token,
            'isAdmin': is_admin
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
    avatar = user.avatar
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
    return JsonResponse({'username': u_name, 'avator': avatar, 'institution': affi, 'bio': bio, 'follows': user_count
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
    user_id = payload.get('id')
    user = User.objects.get(field_id=payload.get('id'))
    data = []
    try:
        users = Follow.objects.filter(scholar_id=user_id)
    except Follow.DoesNotExist:
        return JsonResponse(data)
    for user1 in users:  # FIXME: for user in users
        user_id = user1.user_id  # FIXME: user_id = user.user.field_id
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            continue
        bio = user.bio
        u_name = user.name
        data1 = {'id': user_id, 'username': u_name, 'bio': bio,
                 'time': user1.create_time}
        data.append(data1)
    return JsonResponse(data, safe=False)


@csrf_exempt
def complainSochlar(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    user = User.objects.get(field_id=payload.get('id'))
    scholar_id = request.POST.get('scholar_id')
    reason = request.POST.get('reason')
    scholar = Scholar.objects.filter(scholar_id=scholar_id).first()
    if scholar is None:
        return JsonResponse({'error': 1, 'message': "学者不存在"})
    complain = Complainauthor()
    complain.user = user
    complain.create_time = datetime.datetime
    complain.audit_time = datetime.datetime
    complain.status = 0
    complain.scholar = scholar
    complain.reason = reason
    complain.save()
    return JsonResponse({'errno': 0, 'msg': "success"})


@csrf_exempt
def complainComment(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    user = User.objects.get(field_id=payload.get('id'))
    comment_id = request.POST.get('comment_id')
    reported_id = request.POST.get('reported_id')
    reported = User.objects.filter(field_id=reported_id).first()
    if reported is None:
        return JsonResponse({'error': 1, 'message': "被举报者不存在"})
    reason = request.POST.get('reason')
    comment = Comment.objects.filter(comment_id=comment_id).first()
    if comment is None:
        return JsonResponse({'error': 1, 'message': "评论不存在"})
    complain = Complaincomment()
    complain.user = user
    complain.create_time = datetime.datetime
    complain.audit_time = datetime.datetime
    complain.status = 0
    complain.comment = comment
    complain.report = user
    complain.reported = reported
    complain.reason = reason
    complain.save()
    return JsonResponse({'errno': 0, 'msg': "success"})


@csrf_exempt
def complainPaper(request):
    if request.method != 'POST':
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    user = User.objects.get(field_id=payload.get('id'))
    paper_id = request.POST.get('paper_id')
    reason = request.POST.get('reason')
    complain = Complainpaper()
    complain.user = user
    complain.create_time = datetime.datetime
    complain.audit_time = datetime.datetime
    complain.status = 0
    complain.paper_id = paper_id
    complain.reason = reason
    complain.save()
    return JsonResponse({'errno': 0, 'msg': "success"})


@csrf_exempt
def sendEmail(request):
    if request.method != 'POST':
        return JsonResponse({'result': 0, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    user = User.objects.get(field_id=payload.get('id'))
    try:
        data_body = request.POST

        email = data_body.get('email')
        if email is None:
            return JsonResponse({'result': 0, 'msg': "请检查你的请求体"})
        if not validate_email(email):
            return JsonResponse({'result': 0, 'msg': "邮箱不合法"})
        send_result = sendCodeEmail(email, user.field_id)
        if send_result == 0:
            result = {'result': 0, 'msg': '发送失败!请检查邮箱格式'}
        else:
            result = {'result': 1, 'msg': '发送成功!请及时在邮箱中查收.'}

        return JsonResponse(result)
    except Exception as e:
        traceback.print_exc()


@csrf_exempt
def checkCode(request):
    if request.method != 'POST':
        return JsonResponse({'result': 0, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    user = User.objects.get(field_id=payload.get('id'))
    try:
        data_body = request.POST

        code = data_body.get('code')
        e = CheckCode(code, user.field_id)
        if e is False:
            return JsonResponse({'error': 1, 'msg': "验证码错误"})
        else:
            return JsonResponse({'msg': "验证码正确"})
    except Exception as e:
        traceback.print_exc()


def admit_code(request):
    if request.method != 'POST':
        return JsonResponse({'result': 0, 'msg': "请求方式错误"})
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    data_body = request.POST

    email = data_body.get('email')
    author_id = data_body.get('author_id')
    name = data_body.get('name')
    if email is None:
        return JsonResponse({'result': 0, 'msg': "请检查你的请求体"})
    if not validate_email(email):
        return JsonResponse({'result': 0, 'msg': "邮箱不合法"})
    now_date = datetime.datetime.now()
    admit = Scholaradmit(user_id=payload.get('id'), author_id=author_id, name=name, email=email,
                         create_time=now_date, status=0)
    admit.save()
    return JsonResponse({'errno': 0, 'msg': "验证成功"})
