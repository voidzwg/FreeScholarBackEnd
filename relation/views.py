# publish/views.py
import datetime
import traceback
import os.path
import simplejson
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from relation.models import User, Scholar, Follow, Comment, Like1, Complainauthor, \
    Complaincomment, Complainpaper, Affiliation, Favorites
from utils.Token import Authentication
from utils.media import *


@csrf_exempt
def test(request):
    if request.method == 'GET':
        try:
            follow = Follow.objects.all()
        except Follow.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "删除失败"})
        return JsonResponse({'errno': len(follow)})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getBaseInfo(request):
    if request.method == 'GET':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        counts = 0
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        bio = user.bio
        u_name = user.name
        avatar = user.avatar
        mail = user.mail
        birthday = user.birthday
        identity = user.identity
        state = user.state
        gender = user.gender
        login_date = user.login_date
        try:
            scholar = Scholar.objects.get(user_id=user_id, status=1)
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
            c_id = likes[i].field_id
            try:
                counts += len(Like1.objects.filter(user_id=c_id))
            except Like1.DoesNotExist:
                counts += 0
        return JsonResponse({'username': u_name, 'avatar': avatar, 'institution': affi, 'bio': bio,
                             'follows': user_count, 'followers': scholar_count, 'likes': counts
                             , 'mail': mail, 'birthday': birthday, 'identity': identity, 'state': state
                                , 'gender': gender, 'login_date': login_date})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getFollows(request):
    if request.method == 'GET':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        data = []
        try:
            users = Follow.objects.filter(user_id=user_id)
        except Follow.DoesNotExist:
            return JsonResponse(data)
        for i in range(len(users)):
            scholar_id = users[i].scholar_id
            try:
                scholar = Scholar.objects.get(field_id=scholar_id, status=1)
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
            avatar = user.avatar
            data1 = {'id': user_id, 'scholar_id': scholar_id, 'institution': affi, 'username': u_name
                , 'avatar': avatar, 'bio': bio,'time': users[i].create_time}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getFollowers(request):
    if request.method == 'GET':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
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
            avatar = user.avatar
            data1 = {'id': user_id, 'username': u_name, 'avatar': avatar, 'bio': bio,
                       'time': users[i].create_time}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def unFocus(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        req = simplejson.loads(request.body)
        aim_id = req['aim_id']
        try:
            follow = Follow.objects.get(scholar_id=aim_id, user_id=user_id)
        except Follow.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "删除失败"})
        follow.delete()
        return JsonResponse({'errno': 0, 'msg': "success"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def focus(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        req = simplejson.loads(request.body)
        aim_id = req['aim_id']
        try:
            Follow.objects.get(scholar_id=aim_id, user_id=user_id)
        except Follow.DoesNotExist:
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            follow = Follow(scholar_id=aim_id, user_id=user_id, create_time=time_str)
            follow.save()
            return JsonResponse({'errno': 0, 'msg': "success"})
        return JsonResponse({'errno': 1, 'msg': "已经关注该学者"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def like(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        req = simplejson.loads(request.body)
        aim_id = req['aim_id']
        try:
            Like1.objects.get(comment_id=aim_id, user_id=user_id)
        except Like1.DoesNotExist:
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            obj = Like1(comment_id=aim_id, user_id=user_id, create_time=time_str)
            obj.save()
            return JsonResponse({'errno': 0, 'msg': "success"})
        return JsonResponse({'errno': 1, 'msg': "已经点赞该条评论"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getUser(request):
    if request.method == 'GET':
        data = []
        users = User.objects.all()
        for i in range(len(users)):
            user_id = users[i].field_id
            name = users[i].name
            mail = users[i].mail
            avatar = users[i].avatar
            state = users[i].state
            data1 = {'id': user_id, 'name': name, 'mail': mail, 'avatar': avatar, 'state': state}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def setNormal(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        user.state = 0
        user.save()
        return JsonResponse({'errno': 0, "msg": "解禁成功"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def setMute(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        user.state = 1
        user.save()
        return JsonResponse({'errno': 0, 'msg': "禁言成功"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def setBan(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        user.state = 2
        user.save()
        return JsonResponse({'errno': 0, 'msg': "封禁成功"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getNum(request):
    if request.method == 'GET':
        try:
            user = len(User.objects.all())
        except User.DoesNotExist:
            user = 0
        try:
            admin = len(User.objects.filter(identity=3))
        except User.DoesNotExist:
            admin = 0
        try:
            scholar = len(Scholar.objects.filter(status=1))
        except Scholar.DoesNotExist:
            scholar = 0
        return JsonResponse({'userNum': user, 'scholarNum': scholar, 'adminNum': admin})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getUserItem(request):
    if request.method == 'GET':
        try:
            num1 = len(Affiliation.objects.filter(status=0))
        except Affiliation.DoesNotExist:
            num1 = 0
        try:
            num2 = len(Scholar.objects.filter(status=0))
        except Scholar.DoesNotExist:
            num2 = 0
        num = num1 + num2
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getScholarItem(request):
    if request.method == 'GET':
        try:
            num1 = len(Complainpaper.objects.filter(status=0))
        except Complainpaper.DoesNotExist:
            num1 = 0
        try:
            num2 = len(Complainauthor.objects.filter(status=0))
        except Complainauthor.DoesNotExist:
            num2 = 0
        num = num1+num2
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def editInfo(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        req = simplejson.loads(request.body)
        name = req['name']
        mail = req['mail']
        birthday = req['birthday']
        gender = req['gender']
        bio = req['bio']
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        user.name = name
        user.mail = mail
        user.birthday = birthday
        user.gender = gender
        user.bio = bio
        user.save()
        return JsonResponse({'errno': 0, "msg": "success"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def changePwd(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        req = simplejson.loads(request.body)
        password_old = req['password_old']
        password1 = req['password1']
        password2 = req['password2']
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        if password_old != user.pwd:
            return JsonResponse({'errno': 1, 'msg': "密码错误"})
        if password1 != password2:
            return JsonResponse({'errno': 1, 'msg': "两次密码不一致"})
        user.pwd = password1
        user.save()
        return JsonResponse({'errno': 0, "msg": "success"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getFavorites(request):
    if request.method == 'GET':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        data = []
        try:
            favorites = Favorites.objects.filter(user_id=user_id)
        except Favorites.DoesNotExist:
            return JsonResponse(data)
        for i in range(len(favorites)):
            _id = favorites[i].field_id
            title = favorites[i].title
            create_time = favorites[i].create_time
            avatar = favorites[i].avatar
            count = favorites[i].count
            data1 = {'id': _id, 'title': title, 'avatar': avatar, 'count': count,
                     'time': create_time}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def newFavorites(request):
    if request.method == 'POST':
        try:
            fail, payload = Authentication.authentication(request.META)
            if fail:
                return JsonResponse(payload)
            user_id = payload.get('id')
            req = simplejson.loads(request.body)
            title = req['title']
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            favorite = Favorites(title=title, create_time=time_str, count=0, user_id=user_id)
            favorite.save()
            return JsonResponse({'errno': 0, 'msg': "创建成功"})
        except Exception as e:
            traceback.print_exc()
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def set_avatar(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        uid = payload.get('id')
        avatar = request.FILES.get('avatar')
        if avatar is None or avatar == '':
            return JsonResponse({'errno': -1, 'msg': "头像不能为空"})
        if not avatar.name.lower().endswith(IMAGE_TAIL):
            return JsonResponse({'errno': -2, 'msg': "文件格式错误"})
        try:
            user = User.objects.get(field_id=uid)
        except Exception as e:
            print(e)
            return JsonResponse({'errno': -3, 'msg': "用户不存在"})
        avatar_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f_') + str(uid) + '_' + avatar.name
        try:
            user.avatar = avatar_name
            user.save()
        except Exception as e:
            print(e)
            return JsonResponse({'errno': -4, 'msg': "未知错误"})
        f = open(os.path.join(settings.MEDIA_ROOT, 'avatars', avatar_name), 'wb')
        for i in avatar.chunks():
            f.write(i)
        f.close()
        return JsonResponse({'errno': 0, 'msg': "上传成功"})
    return JsonResponse({'errno': 1001, 'msg': "请求方式错误"})

