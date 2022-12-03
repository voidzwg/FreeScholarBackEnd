

# publish/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from relation.models import User, Scholar, Follow, Comment, Like1


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
        user_id = request.POST.get('user_id')  # 获取请求数据
        aim_id = request.POST.get('aim_id')
        try:
            Follow.objects.get(scholar_id=aim_id, user_id=user_id).delete()
        except Follow.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "删除失败"})
        return JsonResponse({'errno': 0, 'msg': "success"})
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
        user_id = request.POST.get('_id')
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
        user_id = request.POST.get('_id')
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
        user_id = request.POST.get('_id')
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
        data = []
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