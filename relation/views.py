# publish/views.py
import datetime
import traceback

import simplejson
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from FreeScholarBackEnd.settings import SECRETS
from publication.views import publication
from relation.models import *
from utils.Token import Authentication
from utils.media import *
from serialization.views import Serialization

@csrf_exempt
def test(request):
    if request.method == 'GET':
        try:
            data = []
            pid = []
            favorites_id = request.GET['favorites_id']
            try:
                res = Collection.objects.filter(favorites=favorites_id)
            except Collection.DoesNotExist:
                res = None
            for i in range(len(res)):
                pid.append(res[i].paper_id)
            papers = publication.search_by_id_list(pid)
            for i in range(len(res)):
                try:
                    col = Paper.objects.get(paper_id=res[i].paper_id)
                except Paper.DoesNotExist:
                    col = None
                    like_count = 0
                    read_count = 0
                    collect_count = 0
                if col is not None:
                    like_count = col.like_count
                    read_count = col.read_count
                    collect_count = col.collect_count
                data1 = {'like_count': like_count, 'read_count': read_count, 'collect_count': collect_count,
                         'paper': papers[i]}
                data.append(data1)
            return JsonResponse(data, safe=False)
        except Exception as e:
            traceback.print_exc()
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
            scholar = Scholar.objects.get(user_id=user_id)
            scholar_id = scholar.field_id
            author_id = scholar.author_id
            affi = scholar.affi
        except Scholar.DoesNotExist:
            affi = None
            scholar_id = None
            author_id = None
        try:
            user_count = len(Follow.objects.filter(user_id=user_id))
        except Follow.DoesNotExist:
            user_count = 0
        try:
            scholar_count = len(Follow.objects.filter(scholar_id=scholar_id))
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
                                , 'gender': gender, 'login_date': login_date, 'scholar_id': scholar_id
                             , 'author_id': author_id})
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

            data1 = {'id': user_id, 'scholar_id': scholar_id, 'institution': affi, 'username': u_name
                , 'avatar': avatar, 'bio': bio, 'time': users[i].create_time}
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
            scholar_id = Scholar.objects.get(user_id=user_id).field_id
        except Scholar.DoesNotExist:
            return JsonResponse(data)
        try:
            users = Follow.objects.filter(scholar_id=scholar_id)
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
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'POST':
        data = []
        req = simplejson.loads(request.body)
        content = req['input']
        users = User.objects.filter(name__icontains=content)
        for i in range(len(users)):
            user_id = users[i].field_id
            if user_id in SECRETS.get("ADMIN"):
                continue
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
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
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
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
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
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
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
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        try:
            user = len(User.objects.all())
        except User.DoesNotExist:
            user = 0
        try:
            admin = len(SECRETS.get('ADMIN'))
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
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        try:
            num1 = len(Affiliation.objects.filter(status=0))
        except Affiliation.DoesNotExist:
            num1 = 0
        try:
            num2 = len(Scholaradmit.objects.filter(status=0))
        except Scholaradmit.DoesNotExist:
            num2 = 0
        num = num1 + num2
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def getReportAll(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
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
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
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
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        try:
            Complainpaper.objects.order_by('-audit_time')
            Complaincomment.objects.order_by('-audit_time')
            Complainauthor.objects.order_by('-audit_time')
            list1 = []
            list2 = []
            list3 = []
            count = 0
            dict = {}
            for complainpaper in Complainpaper.objects.all():
                if complainpaper.audit_time is not None:
                    dict[complainpaper.audit_time] = complainpaper.field_id
                list1.append(complainpaper)
                count += 1
                if count > 4:
                    break
            count=0
            for complaincomment in Complaincomment.objects.all():
                if complaincomment.audit_time is not None:
                    dict[complaincomment.audit_time] = complaincomment.field_id
                list2.append(complaincomment)
                count += 1
                if count > 4:
                    break
            count=0
            for complainauthor in Complainauthor.objects.all():
                if complainauthor.audit_time is not None:
                    dict[complainauthor.audit_time] = complainauthor.field_id
                list3.append(complainauthor)
                count += 1
                if count > 4:
                    break
            result = []
            keys = list(dict.keys())
            keys.sort(reverse=True)
            admin_avatar=User.objects.get(field_id=21).avatar
            count=0
            for key in keys:
                print(key)
                for i in list1:
                    if i.audit_time == key:
                        if i.status == 0:
                            type = 0
                            tmp = {
                                'type': type,
                                'id': i.field_id,
                                'name':i.user.user.name,
                                'avatar':i.user.user.avatar,
                                'time':i.audit_time,
                            }
                        else:
                            type = 2
                            tmp = {
                                'type': type,
                                'id': i.field_id,
                                'name':"admin",
                                'avatar':admin_avatar,
                                'time':i.audit_time
                            }
                        result.append(tmp)
                for i in list2:
                    if i.audit_time == key:
                        if i.status == 0:
                            type = 1
                            tmp = {
                                'type': type,
                                'id': i.field_id,
                                'name': i.user.user.name,
                                'avatar': i.user.user.avatar,
                                'time': i.audit_time
                            }
                        else:
                            type = 3
                            tmp = {
                                'type': type,
                                'id': i.field_id,
                                'name':"admin",
                                'avatar': admin_avatar,
                                'time': i.audit_time
                            }
                        result.append(tmp)
                for i in list3:
                    if i.audit_time == key:
                        if i.status == 0:
                            type = 0
                            tmp={
                                'type': type,
                                'id': i.field_id,
                                'name': i.user.user.name,
                                'avatar': i.user.user.avatar,
                                'time': i.audit_time
                            }
                        else:
                            type = 2
                            tmp = {
                                'type': type,
                                'id': i.field_id,
                                'name':"admin",
                                'avatar':admin_avatar,
                                'time': i.audit_time
                            }
                        result.append(tmp)
                count += 1
                if count > 4:
                    break

            return JsonResponse({'result': result})
        except Exception as e:
            traceback.print_exc()
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})



@csrf_exempt
def getScholarItem(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
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
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        req = simplejson.loads(request.body)
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
            favorites = Favorites.objects.filter(title=title, user_id=user_id)
            if len(favorites) > 0:
                return JsonResponse({'errno': 1, 'msg': "与现有收藏夹重名"})
            curr_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
            favorite = Favorites(title=title, create_time=time_str, count=0, user_id=user_id, avatar=DEFAULT_COVERIMG)
            favorite.save()
            return JsonResponse({'errno': 0, 'msg': "创建成功"})
        except Exception as e:
            traceback.print_exc()
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getCollectFavorites(request):
    if request.method == 'GET':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        user_id = payload.get('id')
        data = []
        try:
            favorites = Collectfavorites.objects.filter(user_id=user_id)
        except Collectfavorites.DoesNotExist:
            return JsonResponse(data)
        for i in range(len(favorites)):
            _id = favorites[i].favorites_id
            favorite = Favorites.objects.get(field_id=_id)
            title = favorite.title
            create_time = favorite.create_time
            avatar = favorite.avatar
            count = favorite.count
            data1 = {'id': _id, 'title': title, 'avatar': avatar, 'count': count,
                     'time': create_time}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def collectFavorites(request):
    if request.method == 'POST':
        try:
            fail, payload = Authentication.authentication(request.META)
            if fail:
                return JsonResponse(payload)
            user_id = payload.get('id')
            req = simplejson.loads(request.body)
            favorites_id = req['favorites_id']
            try:
                Collectfavorites.objects.get(favorites_id=favorites_id, user_id=user_id)
            except Collectfavorites.DoesNotExist:
                favorite = Collectfavorites(favorites_id=favorites_id, user_id=user_id)
                favorite.save()
                return JsonResponse({'errno': 0, 'msg': "收藏成功"})
            return JsonResponse({'errno': 1, 'msg': "已经收藏该收藏夹"})
        except Exception as e:
            traceback.print_exc()
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})



@csrf_exempt
def getUserItemAll(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        # fail, payload = Authentication.authentication(request.META)
        # if fail:
        #     return JsonResponse(payload)
        # user_id = payload.get('id')
        try:
            num1 = len(Affiliation.objects.filter(status=2) | Affiliation.objects.filter(status=1))
        except Affiliation.DoesNotExist:
            num1 = 0
        try:
            num2 = len(Scholaradmit.objects.filter(status=1) | Scholaradmit.objects.filter(status=2))
        except Scholaradmit.DoesNotExist:
            num2 = 0
        num = num1+num2
        return JsonResponse({'num': num})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getAllAccusationRecords(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        try:
            data = []
            try:
                res1 = Complaincomment.objects.all()
            except Complaincomment.DoesNotExist:
                res1 = None
            res1 = serializers.serialize("json", res1, ensure_ascii=False)
            res1 = simplejson.loads(res1)
            data.append(res1)
            try:
                res2 = Complainauthor.objects.all()
            except Complainauthor.DoesNotExist:
                res2 = None
            res2 = serializers.serialize("json", res2, ensure_ascii=False)
            res2 = simplejson.loads(res2)
            data.append(res2)
            return JsonResponse(data, safe=False)
        except Exception as e:
            traceback.print_exc()
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getAllAppealRecords(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        data = []
        try:
            res1 = Complainpaper.objects.all()
        except Complainpaper.DoesNotExist:
            res1 = None
        res1 = serializers.serialize("json", res1, ensure_ascii=False)
        res1 = simplejson.loads(res1)
        data.append(res1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def getAllInstitutionApplication(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        data = []
        try:
            res1 = Affiliation.objects.all()
        except Affiliation.DoesNotExist:
            res1 = None
        res1 = serializers.serialize("json", res1, ensure_ascii=False)
        res1 = simplejson.loads(res1)
        data.append(res1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def getAllScholarApplication(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        data = []
        try:
            res1 = Scholaradmit.objects.all()
        except Scholaradmit.DoesNotExist:
            res1 = None
        res1 = serializers.serialize("json", res1, ensure_ascii=False)
        res1 = simplejson.loads(res1)
        data.append(res1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getPendingAccusationRecords(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        try:
            data = []
            try:
                res1 = Complaincomment.objects.filter(status=0)
            except Complaincomment.DoesNotExist:
                res1 = None
            res1 = serializers.serialize("json", res1, ensure_ascii=False)
            res1 = simplejson.loads(res1)
            data.append(res1)
            try:
                res2 = Complainauthor.objects.filter(status=0)
            except Complainauthor.DoesNotExist:
                res2 = None
            res2 = serializers.serialize("json", res2, ensure_ascii=False)
            res2 = simplejson.loads(res2)
            data.append(res2)
            return JsonResponse(data, safe=False)
        except Exception as e:
            traceback.print_exc()
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def getPendingAppealRecords(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        data = []
        try:
            res1 = Complainpaper.objects.filter(status=0)
        except Complainpaper.DoesNotExist:
            res1 = None
        res1 = serializers.serialize("json", res1, ensure_ascii=False)
        res1 = simplejson.loads(res1)
        data.append(res1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def getPendingInstitutionApplication(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        data = []
        try:
            res1 = Affiliation.objects.filter(status=0)
        except Affiliation.DoesNotExist:
            res1 = None
        res1 = serializers.serialize("json", res1, ensure_ascii=False)
        res1 = simplejson.loads(res1)
        data.append(res1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def getPendingScholarApplication(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        data = []
        try:
            res1 = Scholaradmit.objects.filter(status=0)
        except Scholaradmit.DoesNotExist:
            res1 = None
        res1 = serializers.serialize("json", res1, ensure_ascii=False)
        res1 = simplejson.loads(res1)
        data.append(res1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


@csrf_exempt
def processRequest(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'POST':
        try:
            user_id = payload.get('id')
            type1 = request.POST.get('type')
            _id = request.POST.get('id')
            res = request.POST.get('agreeOrRefuse')
            if res == "True":
                res = True
            else:
                res = False
            reply = request.POST.get('reply')
            if type1 == "0":
                try:
                    obj = Complaincomment.objects.get(field_id=_id)
                except Complaincomment.DoesNotExist:
                    return JsonResponse({'errno': 1, 'msg': "该事项不存在"})
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                if res:
                    obj.status = 2
                else:
                    obj.status = 1
                obj.audit_time = time_str
                obj.reply = reply
                obj.save()
            elif type1 == "1":
                try:
                    obj = Complainauthor.objects.get(field_id=_id)
                except Complainauthor.DoesNotExist:
                    return JsonResponse({'errno': 1, 'msg': "该事项不存在"})
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                if res:
                    obj.status = 2
                else:
                    obj.status = 1
                obj.audit_time = time_str
                obj.reply = reply
                obj.save()
            elif type1 == "2":
                try:
                    obj = Complainpaper.objects.get(field_id=_id)
                except Complainpaper.DoesNotExist:
                    return JsonResponse({'errno': 1, 'msg': "该事项不存在"})
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                if res:
                    obj.status = 2
                else:
                    obj.status = 1
                obj.audit_time = time_str
                obj.reply = reply
                obj.save()
            elif type1 == "3":
                try:
                    obj = Affiliation.objects.get(field_id=_id)
                except Affiliation.DoesNotExist:
                    return JsonResponse({'errno': 1, 'msg': "该事项不存在"})
                if res:
                    obj.status = 2
                else:
                    obj.status = 1
                obj.admin_id = user_id
                obj.save()
            elif type1 == "4":
                curr_time = datetime.datetime.now()
                time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
                try:
                    obj = Scholaradmit.objects.get(field_id=_id)
                except Scholaradmit.DoesNotExist:
                    return JsonResponse({'errno': 1, 'msg': "该事项不存在"})
                if res:
                    obj.status = 2
                    author_id = obj.author_id
                    user_id1 = obj.user_id
                    name = obj.name
                    try:
                        obj1 = Scholar.objects.filter(author_id=author_id) | Scholar.objects.filter(user_id=user_id1)
                        if len(obj1) > 0:
                            obj.status = 1
                            obj.reply = "该学者已存在或该用户已经是学者"
                            obj.audit_time = time_str
                            obj.save()
                            return JsonResponse({'errno': 1, 'msg': "该学者已存在或该用户已经是学者"})
                    except Scholar.DoesNotExist:
                        name = Scholaradmit.name
                    Scholar.objects.create(user_id=user_id1, author_id=author_id,
                                            name=name, affi="{}", claim_time=time_str)
                else:
                    obj.status = 1
                obj.audit_time = time_str
                obj.reply = reply
                obj.save()
            return JsonResponse({'errno': 0, 'msg': "处理成功"})
        except Exception as e:
            traceback.print_exc()
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def showFavorites(request):
    if request.method == 'GET':
        data = []
        pid = []
        favorites_id = request.GET['favorites_id']
        try:
            res = Collection.objects.filter(favorites=favorites_id)
        except Collection.DoesNotExist:
            res = None
        for i in range(len(res)):
            pid.append(res[i].paper_id)
        papers = publication.search_by_id_list(pid)
        for i in range(len(res)):
            try:
                col = Paper.objects.get(paper_id=res[i].paper_id)
            except Paper.DoesNotExist:
                col = None
                like_count = 0
                read_count = 0
                collect_count = 0
            if col is not None:
                like_count = col.like_count
                read_count = col.read_count
                collect_count = col.collect_count
            data1 = {'like_count': like_count, 'read_count': read_count, 'collect_count': collect_count,
                     'paper': papers[i]}
            data.append(data1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def getHistoryByUserId(request):
    if request.method == 'POST':
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        _id = payload.get('id')
        data = []
        try:
            res = Viewhistory.objects.filter(user_id=_id)
        except Viewhistory.DoesNotExist:
            res = None
        for i in range(len(res)):
            data.append({'_id': res[i].field_id, 'user_id': res[i].user_id, 'paper_id': res[i].paper_id,
                     'time': res[i].time})
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def deleteHistory(request):
    if request.method == 'POST':
        _id = request.POST.get('history_id')
        try:
            Viewhistory.objects.get(field_id=_id).delete()
        except Viewhistory.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "历史记录不存在"})
        return JsonResponse({'errno': 0, 'msg': "删除成功"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def getSolvedTaskNum(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if payload.get('admin') is False:
        return JsonResponse({'errno': -999, 'msg': "没有管理员权限"})
    if request.method == 'GET':
        data = []
        now = datetime.datetime.now().date()
        x = now
        for i in range(7):
            y = x + datetime.timedelta(days=1)
            try:
                num1 = len(Complaincomment.objects.filter(audit_time__gte=x, audit_time__lte=y))
            except Complaincomment.DoesNotExist:
                num1 = 0
            try:
                num2 = len(Complainauthor.objects.filter(audit_time__gte=x, audit_time__lte=y))
            except Complainauthor.DoesNotExist:
                num2 = 0
            try:
                num3 = len(Complainpaper.objects.filter(audit_time__gte=x, audit_time__lte=y))
            except Complainpaper.DoesNotExist:
                num3 = 0
            num = num1 + num2 + num3
            data.append(num)
            x = x - datetime.timedelta(days=1)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


def deleteFavorites(request):
    fail, payload = Authentication.authentication(request.META)
    if fail:
        return JsonResponse(payload)
    if request.method == 'POST':
        favorites_id = request.POST.get('favorites_id')
        try:
            Favorites.objects.get(field_id=favorites_id).delete()
        except Favorites.DoesNotExist:
            return JsonResponse({'errno': 1, 'msg': "收藏夹不存在"})
        return JsonResponse({'errno': 0, 'msg': "删除成功"})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})