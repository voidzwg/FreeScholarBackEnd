import datetime

from django.shortcuts import render
from django.http import JsonResponse
import traceback
from utils.Token import Authentication
from publication.models import *
from utils import Rating
from FreeScholarBackEnd.settings import *
import uuid


class publication:
    @staticmethod
    def GetWord(request):
        if request.method == 'POST':
            try:
                para = eval(request.body)
                list = para['condition']
                for i in list:
                    word = i['input']
                    field = Field.objects.filter(name=word).first()
                    if field is None:
                        field = Field()
                        field.name = i['input']
                        field.type = i['field']
                        field.count = 1
                        field.save()
                        field.SavingRatingWord()
                    else:
                        field.count += 1
                        field.save()
                        field.SavingRatingWord()
                return JsonResponse({'message': "成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'errno': '1'})

    @staticmethod
    def search(request):
        if request.method == 'POST':
            try:
                para = eval(request.body)
                page = int(para['page'])
                page = page - 1
                # output:dict数据
                list = para['condition']
                should = {}
                shoulds = []
                for i in list:
                    input = i['input']
                    if not input:
                        continue
                    if i['field'] == 'author':
                        field = i['field'] + 's.name'
                    elif i['field'] == 'venue':
                        field = i['field'] + '.raw'
                    elif i['field'] == 'org':
                        field = 'authors' + '.org'
                    else:
                        field = i['field']
                    if i['type'] == 'OR':
                        if should:
                            shoulds.append(should)
                        if (i['field']) == 'year':
                            should = {
                                "bool":
                                    {
                                        "must":
                                            [
                                                {
                                                    "range": {
                                                        "year": {
                                                            "gte": i['input'][0],
                                                            "lte": i['input'][1]
                                                        }
                                                    }
                                                }
                                            ]
                                    }
                            }
                        else:
                            should = {
                                "bool":
                                    {
                                        "must":
                                            [
                                                {
                                                    "match": {field: input}
                                                }
                                            ]
                                    }
                            }
                        shoulds.append(should)
                    elif i['type'] == 'AND':
                        if (i['field']) == 'year':
                            match = {
                                "range": {
                                    "year": {
                                        "gte": i['input'][0],
                                        "lte": i['input'][1]
                                    }
                                }
                            }
                        else:
                            match = {"match": {field: input}}
                        should['bool']['must'].append(match)
                    elif i['type'] == 'NOR':
                        if (i['field']) == 'year':
                            match = {
                                "bool":
                                    {
                                        "must_not":
                                            [
                                                {
                                                    "range": {
                                                        "year": {
                                                            "gte": i['input'][0],
                                                            "lte": i['input'][1]
                                                        }
                                                    }
                                                }
                                            ]
                                    }
                            }
                        else:
                            match = {
                                "bool":
                                    {
                                        "must_not":
                                            [
                                                {
                                                    "match": {field: input}
                                                }
                                            ]
                                    }
                            }
                        should['bool']['must'].append(match)
                filter = para['filter']
                filters = []
                for f in filter:
                    type = 'term'
                    field = f['field']
                    if f['field'] == 'venue':
                        field = f['field'] + '.raw'
                    elif f['field'] == 'org':
                        field = 'authors' + '.org'
                        type = 'match_phrase'
                    elif f['field'] == 'year':
                        type = 'range'
                    elif f['field'] == 'keyword':
                        field = 'keywords'
                    if f['field'] != 'org':
                        field = field + '.keyword'
                    if f['field'] == 'year':
                        match = {
                            "range": {
                                "year": {
                                    "gte": f['value'][0],
                                    "lte": f['value'][1]
                                }
                            }
                        }
                        for s in shoulds:
                            s['bool']['must'].append(match)
                    elif f['field'] == 'lang':
                        match = {
                            "term": {
                                "lang": f['value']
                            }
                        }
                        for s in shoulds:
                            s['bool']['must'].append(match)
                    else:
                        fq = {
                            type: {
                                field: f['value']
                            }
                        }
                        filters.append(fq)
                sort = []
                if 'sort' in para:
                    if para['sort'] == 'time':
                        s = {
                            "year": {"order": "desc"}
                        }
                    elif para['sort'] == 'citation':
                        s = {
                            "n_citation": {"order": "desc"}
                        }
                    sort.append(s)
                body = {
                    "query": {
                        "function_score": {
                            "query": {
                                "bool": {
                                    "should": shoulds,
                                    "filter": filters,
                                },

                            },

                            "functions": [
                                {"field_value_factor": {
                                    "field": "n_citation",
                                    "modifier": "log1p",
                                    "factor": 0.1,
                                    "missing": 0,
                                }},

                                {
                                    "weight": 0,
                                    "filter": {
                                        "bool": {
                                            "must_not": {
                                                "exists": {
                                                    "field": "abstract"
                                                }
                                            }
                                        }
                                    }
                                },

                            ],
                            "boost_mode": "multiply",

                        },

                    },
                    "sort": sort,
                    "from": str(page),
                    "size": 20,
                    "min_score": 5
                }
                resp = client.search(index='paper', body=body)
                return JsonResponse(resp['hits'])
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'errno': '1'})

    @staticmethod
    def HotPaper(request):
        if request.method == 'POST':
            try:
                Top_paper = Rating.rating_connection.zrange('HotPaper', 0, 10, desc=True, withscores=True)
                paper_data = []
                for i in Top_paper:
                    field_id = i[0].decode()
                    paper = Paper.objects.filter(field_id=field_id).first()
                    if paper is None:
                        continue
                    paper_data.append({'title': paper.paper_name, 'id': paper.paper_id, 'read_count': paper.read_count,
                                       'like_count': paper.like_count, 'collect_count': paper.collect_count})
                result = {
                    'paper': paper_data
                }
                return JsonResponse(result)
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    @staticmethod
    def HotWord(request):
        if request.method == 'POST':
            try:
                Top_paper = Rating.rating_connection.zrange('HotWord', 0, 10, desc=True, withscores=True)
                word_data = []
                for i in Top_paper:
                    field_id = i[0].decode()
                    field = Field.objects.get(field_id=field_id)
                    word_data.append({'word_name': field.name,'value':field.count})
                result = {
                    'word': word_data
                }
                return JsonResponse(result)
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    @staticmethod
    def ReadPaper(request):
        if request.method == 'POST':
            login = True
            fail, payload = Authentication.authentication(request.META)
            if fail:
                login = False
                uid = payload.get('id')
            else:
                uid = None
            data = request.body.decode()
            data_body = json.loads(data)
            paper_id = data_body.get('paper_id')
            paper_name = data_body.get('paper_name')
            if login:
                vh = Viewhistory(user_id=uid, paper_id=paper_id, time=datetime.datetime.now())
                vh.save()
            paper = Paper.objects.filter(paper_id=paper_id).first()
            comments = Comment.objects.filter(paper_id=paper_id)
            comment_result = []
            for comment in comments:
                tmp = {
                    "comment_id":comment.field_id,
                    "user_id":comment.user.field_id,
                    "avatar": comment.user.avatar,
                    "username": comment.user.name,
                    "text": comment.content,
                    "likecount":comment.count,
                }
                if login:
                    like1 = Like1.objects.filter(user_id=uid, comment=comment).first()
                    if like1 is None:
                        isliked = False
                    else:
                        isliked = True
                    tmp['liked'] = isliked
                comment_result.append(tmp)
            if paper is None:
                paper = Paper()
                paper.paper_id = paper_id
                paper.paper_name = paper_name
                paper.read_count = 1
                paper.like_count = 0
                paper.collect_count = 0
                paper.save()
                paper.save_paper_data()
            else:
                paper.read_count += 1
                paper.save()
                paper.save_paper_data()

            json_data = {
                'like_count': paper.like_count,
                'read_count': paper.read_count,
                'collect_count': paper.collect_count,
                'comment': comment_result
            }
            if login:
                like = Like.objects.filter(user_id=uid, paper=paper).first()
                if like is None:
                    isLiked1 = False
                else:
                    isLiked1 = True
                collect = Collection.objects.filter(user_id=uid, paper_id=paper_id).first()
                if collect is None:
                    isCollected = False
                else:
                    isCollected = True
                json_data['isLiked'] = isLiked1
                json_data['isCollected'] = isCollected
            return JsonResponse(json_data)

    @staticmethod
    def MakeComment(request):
        if request.method == 'POST':
            fail, payload = Authentication.authentication(request.META)
            if fail:
                return JsonResponse(payload)
            try:
                user_id = payload.get('id')
                user = User.objects.get(field_id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'errno': 1, 'msg': "用户不存在"})
            try:
                data_body = request.POST
                paper_id = data_body.get('paper_id')
                content = data_body.get('content')
                paper = Paper.objects.filter(paper_id=paper_id).first()
                if paper is None:
                    return JsonResponse({'error': 0, 'message': "文章不存在"})
                else:
                    comment = Comment()
                    comment.user = user
                    comment.paper_id = paper_id
                    comment.count = 0
                    comment.content = content
                    comment.create_time = datetime.datetime.now()
                    comment.save()
                return JsonResponse({'message': "评论成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    @staticmethod
    def LikeComment(request):
        if request.method == 'POST':
            fail, payload = Authentication.authentication(request.META)
            if fail:
                return JsonResponse(payload)
            try:
                user_id = payload.get('id')
                user = User.objects.get(field_id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'errno': 1, 'msg': "用户不存在"})
            try:
                data_body = request.POST
                comment_id = data_body.get('comment_id')
                comment = Comment.objects.filter(field_id=comment_id).first()
                if comment is None:
                    return JsonResponse({'error': 0, 'message': "评论不存在"})
                like1 = Like1.objects.filter(user=user, comment=comment).first()
                if like1 is None:
                    like11 = Like1()
                    like11.comment = comment
                    like11.user = user
                    like11.create_time = datetime.datetime.now()
                    like11.save()
                    comment.count += 1
                    comment.save()
                    return JsonResponse({'msg': "点赞成功"})
                else:
                    return JsonResponse({'msg': "你已经赞过了"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    @staticmethod
    def LikePaper(request):
        if request.method == 'POST':
            fail, payload = Authentication.authentication(request.META)
            if fail:
                return JsonResponse(payload)
            try:
                user_id = payload.get('id')
                user = User.objects.get(field_id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'errno': 1, 'msg': "用户不存在"})
            try:
                data_body = request.POST
                paper_id = data_body.get('paper_id')
                paper = Paper.objects.filter(paper_id=paper_id).first()
                if paper is None:
                    return JsonResponse({'error': 0, 'message': "文章不存在"})
                like = Like.objects.filter(user=user, paper=paper).first()
                if like is None:
                    like_1 = Like()
                    like_1.paper = paper
                    like_1.user = user
                    paper.like_count += 1
                    paper.save_paper_data()
                    paper.save()
                    like_1.save()
                    return JsonResponse({'message': "点赞成功"})
                else:
                    like.delete()
                    paper.like_count -= 1
                    paper.save()
                    paper.save_paper_data()
                    return JsonResponse({'message': "取消点赞成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    @staticmethod
    def CollectPaper(request):
        if request.method == 'POST':
            fail, payload = Authentication.authentication(request.META)
            if fail:
                return JsonResponse(payload)
            try:
                user_id = payload.get('id')
                user = User.objects.get(field_id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'errno': 1, 'msg': "用户不存在"})
            try:
                data_body = request.POST
                paper_id = data_body.get('paper_id')
                favorites_id = data_body.get('favorites_id')
                paper = Paper.objects.filter(paper_id=paper_id).first()
                favorite = Favorites.objects.filter(field_id=favorites_id).first()
                if paper is None:
                    return JsonResponse({'error': 0, 'message': "文章不存在"})
                elif favorite is None:
                    return JsonResponse({'error': 0, 'message': "收藏夹不存在"})
                collection = Collection.objects.filter(user=user, paper_id=paper_id, favorites=favorite).first()
                if collection is not None:
                    return JsonResponse({'error': 0, 'msg': "收藏关系已存在"})
                else:
                    paper.collect_count += 1
                    paper.save_paper_data()
                    paper.save()
                    collection = Collection()
                    collection.paper_id = paper_id
                    collection.user = user
                    collection.favorites = favorite
                    collection.time = datetime.datetime.now()
                    favorite.count += 1
                    favorite.save()
                    collection.save()
                return JsonResponse({'message': "收藏成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    @staticmethod
    def UnCollectPaper(request):
        if request.method == 'POST':
            fail, payload = Authentication.authentication(request.META)
            if fail:
                return JsonResponse(payload)
            try:
                user_id = payload.get('id')
                user = User.objects.get(field_id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'errno': 1, 'msg': "用户不存在"})
            try:
                data_body = request.POST
                paper_id = data_body.get('paper_id')
                paper = Paper.objects.filter(paper_id=paper_id).first()
                if paper is None:
                    return JsonResponse({'error': 0, 'message': "文章不存在"})
                favorites_id = data_body.get('favorites_id')
                favorite = Favorites.objects.filter(field_id=favorites_id).first()
                if favorite is None:
                    return JsonResponse({'error': 0, 'message': "收藏夹不存在"})
                collection = Collection.objects.filter(user=user, paper_id=paper_id, favorites=favorite).first()
                if collection is None:
                    return JsonResponse({'error': 0, 'message': "不具备收藏关系"})
                if favorite is None:
                    return JsonResponse({'error': 0, 'message': "收藏夹不存在"})
                else:
                    paper.collect_count -= 1
                    paper.save_paper_data()
                    paper.save()
                    favorite.count -= 1
                    favorite.save()
                    collection.delete()
                return JsonResponse({'message': "取消收藏成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    @staticmethod
    def search_by_id_list(idList):
        body = {
            "query": {
                "terms": {
                    "id": idList
                }
            },
            "from": 0,
            "size": 10000,
        }
        resp = client.search(index='paper', body=body)
        hits = resp['hits']['hits']
        return hits

    @staticmethod
    def getVenueListByIdList(request):
        try:
            if request.method == 'POST':
                para = eval(request.body)
                idList = para['idList']
                vlist = []
                hits = publication.search_by_id_list(idList)
                for hit in hits:
                    if 'venue' in hit['_source']:
                        if 'raw' in hit['_source']['venue']:
                            v = hit['_source']['venue']['raw'].strip()
                            if not (v in vlist):
                                vlist.append(v)
                return JsonResponse({'data': vlist})
            else:
                return JsonResponse({'errno': '1'})
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    def getKeyListByIdList(request):
        try:
            if request.method == 'POST':
                para = eval(request.body)
                idList = para['idList']
                hits = publication.search_by_id_list(idList)
                klist = []
                for hit in hits:
                    if 'keywords' in hit['_source']:
                        for k in hit['_source']['keywords']:
                            k = k.strip()
                            if not (k in klist):
                                klist.append(k)
                return JsonResponse({'data': klist})
            else:
                return JsonResponse({'errno': '1'})
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    def getOrgListByIdList(request):
        try:
            if request.method == 'POST':
                para = eval(request.body)
                idList = para['idList']
                hits = publication.search_by_id_list(idList)
                olist = []
                for hit in hits:
                    for a in hit['_source']['authors']:
                        if ('org' in a):
                            list = a['org'].split(',')
                            for i in list:
                                if ('University' in i or 'Université' in i or '大学' in i):
                                    i = i.strip()
                                    if not (i in olist):
                                        olist.append(i)
                return JsonResponse({'data': olist})
            else:
                return JsonResponse({'errno': '1'})
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    def getPaperByIdList(request):
        try:
            if request.method == 'POST':
                para = eval(request.body)
                idList = para['idList']
                resp = publication.search_by_id_list(idList)
                data = []
                for h in resp:
                    data.append(h['_source'])
                return JsonResponse({'data': data})
            else:
                return JsonResponse({'errno': '1'})
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    def getPaperById(request):
        try:
            if request.method == 'POST':

                id = request.POST.get('id')
                body = {
                    "query": {
                        "term": {
                            "id": id
                        }
                    }
                }
                resp = client.search(index='paper', body=body)
                if resp['hits']['total']['value'] > 0:
                    return JsonResponse({'paper': resp['hits']['hits'][0]['_source']})
            else:
                return JsonResponse({'errno': '1'})
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    def addPub(request):
        try:
            if request.method == 'POST':
                para = eval(request.body)
                id = uuid.uuid1().hex
                document = {}
                document["id"] = id
                document["title"] = para['title']
                document["authors"] = para['authors']
                if "abstract" in para:
                    document["abstract"] = para['abstract']
                if "year" in para:
                    document["year"] = para["year"]
                if "url" in para:
                    document["url"] = para["year"]
                if "venue" in para:
                    document["venue"] = para["venue"]
                if "keywords" in para:
                    document["keywords"] = para["keywords"]
                if "n_citation" in para:
                    document["n_citation"] = para["n_citation"]
                if "lang" in para:
                    document["lang"] = para["lang"]
                if "doi" in para:
                    document["doi"] = para["doi"]
                if "issn" in para:
                    document["issn"] = para["issn"]
                if "pdf" in para:
                    document["pdf"] = para["pdf"]
                resp = client.index(index='paper', document=document)
                if resp['result'] == 'created':
                    return JsonResponse({'errno': '0', "msg": "成功"})
                else:
                    return JsonResponse({'errno': '2', "msg": "失败"})
            else:
                return JsonResponse({'errno': '1', "msg": "请求方式错误"})

        except Exception as e:
            traceback.print_exc()
