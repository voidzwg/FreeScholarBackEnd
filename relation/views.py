# publish/views.py
import simplejson
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from relation.models import User, Scholar, Follow, Comment, Like1, Complainauthor, \
    Complaincomment, Complainpaper


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
        user_id = request.GET['user_id']  # 获取请求数据
        counts = 0
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        bio = user.bio
        u_name = user.name
        avatar = user.avatar
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
        return JsonResponse({'username': u_name, 'avatar': avatar, 'institution': affi, 'bio': bio,
                             'follows': user_count, 'followers': scholar_count, 'likes': counts})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getFollows(request):
    if request.method == 'GET':
        user_id = request.GET['user_id']  # 获取请求数据
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
            avatar = user.avatar
            data1 = {'id': user_id, 'institution': affi, 'username': u_name, 'avatar': avatar, 'bio': bio,
                     'time': users[i].create_time}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getFollowers(request):
    if request.method == 'GET':
        user_id = request.GET['user_id']  # 获取请求数据
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
        req = simplejson.loads(request.body)
        user_id = req['user_id']  # 获取请求数据
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
        req = simplejson.loads(request.body)
        user_id = req['user_id']  # 获取请求数据
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
        req = simplejson.loads(request.body)
        user_id = req['user_id']  # 获取请求数据
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
        req = simplejson.loads(request.body)
        user_id = req['_id']
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
        req = simplejson.loads(request.body)
        user_id = req['_id']
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
        req = simplejson.loads(request.body)
        user_id = req['_id']
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
            scholar = len(Scholar.objects.all())
        except Scholar.DoesNotExist:
            scholar = 0
        return JsonResponse({'userNum': user, 'scholarNum': scholar, 'adminNum': admin})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getUserItem(request):
    if request.method == 'GET':
        try:
            num = len(Complaincomment.objects.filter(status=0))
        except Complaincomment.DoesNotExist:
            num = 0
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def getReportAll(request):
    if request.method == 'GET':
        try:
            num1 = len(Complaincomment.objects.filter(status=1))
        except Complaincomment.DoesNotExist:
            num1 = 0
        try:
            num2 = len(Complainauthor.objects.filter(status=1))
        except Complainauthor.DoesNotExist:
            num2 = 0
        num = num1 + num2
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getComplainAll(request):
    if request.method == 'GET':
        try:
            num = len(Complainpaper.objects.filter(status=1))
        except Complainpaper.DoesNotExist:
            num = 0
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getRecentRecord(request):
    if request.method == 'GET':
        try:
            Complainpaper.objects.all.order_by('-create_time')
            Complaincomment.objects.all.order_by('-create_time')
            Complainauthor.objects.all.order_by('-create_time')
        except Complainpaper.DoesNotExist:
            num1 = 0
        try:
            num2 = len(Complainauthor.objects.filter(status=0))
        except Complainauthor.DoesNotExist:
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
        num = num1 + num2
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def editInfo(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        user_id = req['id']
        name = req['name']
        mail = req['mail']
        birthday = req['birthday']
        birth = datetime.date(*map(int, birthday.split('-')))
        gender = req['gender']
        bio = req['bio']
        try:
            user = User.objects.get(field_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "用户不存在"})
        user.name = name
        user.mail = mail
        user.birthday = birth
        user.gender = gender
        user.bio = bio
        user.save()
        return JsonResponse({'errno': 0, "msg": "success"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def changePwd(request):
    if request.method == 'POST':
        req = simplejson.loads(request.body)
        user_id = req['id']
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
