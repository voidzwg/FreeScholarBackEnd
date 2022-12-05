from django.shortcuts import render
from django.http import JsonResponse
import traceback
# Create your views here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from utils.Token import Authentication
from utils import Rating

from publication.models import *
from utils import Rating
import sys, io
from publication import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
client = Elasticsearch('http://139.9.134.209:9200')


class publication:

    def GetWord(request):
        if request.method == 'POST':
            try:
                para = eval(request.body)
                list = para['condition']
                for i in list:
                    word=i['input']
                    field = Field.objects.filter(name=word).first()
                    if field is None:
                        field = Field()
                        field.name=i['input']
                        field.type=i['field']
                        field.count = 1
                        field.save()
                        field.SavingRatingWord()
                    else:
                        field.count+=1
                        field.save()
                        field.SavingRatingWord()
                return JsonResponse({'message': "成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'errno': '1'})

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
                body = {
                    "query": {
                        "function_score": {
                            "query": {
                                "bool": {
                                    "should": shoulds
                                }
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
                                }

                            ],
                            "boost_mode": "multiply"
                        },
                    },
                    "from": str(page),
                    "size": 20,

                }
                resp = client.search(index='paper', body=body)
                return JsonResponse(resp['hits'], safe=False)
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'errno': '1'})

    def HotPaper(request):
        if request.method == 'POST':
            try:
                Top_paper = Rating.rating_connection.zrange('HotPaper', 0, 10, desc=True, withscores=True)
                paper_data = []
                for i in Top_paper:
                    field_id = i[0].decode()
                    paper=Paper.objects.get(field_id=field_id)
                    paper_data.append({'paper_name': paper.paper_name})
                result = {
                    'paper': paper_data
                }
                return JsonResponse(result)
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    def HotWord(request):
        if request.method == 'POST':
            try:
                Top_paper = Rating.rating_connection.zrange('HotWord', 0, 10, desc=True, withscores=True)
                word_data = []
                for i in Top_paper:
                    field_id = i[0].decode()
                    field = Field.objects.get(field_id=field_id)
                    word_data.append({'word_name': field.name})
                result = {
                    'paper': word_data
                }
                return JsonResponse(result)
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    def ReadPaper(request):
        if request.method == 'POST':
            try:
                data_body = request.POST
                paper_id = data_body.get('paper_id')
                paper_name = data_body.get('paper_name')
                paper = Paper.objects.filter(paper_id=paper_id).first()
                if paper is None:
                    paper = Paper()
                    paper.paper_id = paper_id
                    paper.paper_name = paper_name
                    paper.read_count = 1
                    paper.like_count = 0
                    paper.collect_count = 0
                    paper.save_paper_data()
                    paper.save()
                else:
                    paper.read_count += 1
                    paper.save_paper_data()
                    paper.save()
                return JsonResponse({'message': "阅读成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

    def LikePaper(request):
        if request.method == 'POST':
            try:
                data_body = request.POST
                paper_id = data_body.get('paper_id')
                paper = Paper.objects.filter(paper_id=paper_id).first()
                if paper is None:
                    return JsonResponse({'error': 0, 'message': "文章不存在"})
                else:
                    paper.like_count += 1
                    paper.save_paper_data()
                    paper.save()
                return JsonResponse({'message': "点赞成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

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
                paper = Paper.objects.filter(paper_id=paper_id).first()
                if paper is None:
                    return JsonResponse({'error': 0, 'message': "文章不存在"})
                else:
                    paper.like_count += 1
                    paper.save_paper_data()
                    paper.save()
                    collection = Collection()
                    collection.paper_id = paper_id
                    collection.user = user
                    collection.save()
                return JsonResponse({'message': "收藏成功"})
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'error': 0, 'message': "请求方式错误"})

