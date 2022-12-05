from django.shortcuts import render
from django.http import JsonResponse
import traceback
# Create your views here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
client = Elasticsearch('http://139.9.134.209:9200')

class publication:
    def search(request):
        if request.method == 'POST':
            try:
                para = eval(request.body)
                page = int(para['page'])
                page = page - 1
                # output:dict数据
                list = para['condition']
                should ={}
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
                        if(i['field']) == 'year':
                            should = {
                                "bool":
                                    {
                                        "must":
                                            [
                                                {
                                                    "range": {
                                                        "year":{
                                                            "gte":i['input'][0],
                                                            "lte":i['input'][1]
                                                        }
                                                    }
                                                }
                                            ]
                                    }
                            }
                        else:
                            should ={
                                    "bool":
                                    {
                                        "must":
                                            [
                                                {
                                                    "match":{field:input}
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
                            match ={"match":{field:input}}
                        should['bool']['must'].append(match)
                    elif i['type'] == 'NOR':
                        if (i['field']) == 'year':
                            match= {
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
                        field = field+'.keyword'
                    if f['field'] == 'year':
                        fq = {
                            type: {
                                "year": {
                                        "gte": f['value'][0],
                                        "lte": f['value'][1]
                                }
                            }
                        }
                    else:
                        fq = {
                            type:{
                                field:f['value']
                            }
                        }
                    filters.append(fq)

                body={
                    "query":{
                        "function_score": {
                            "query":{
                                "bool": {
                                    "should": shoulds,
                                    "filter": filters
                                },

                            },

                            "functions":[
                                {"field_value_factor": {
                                "field": "n_citation",
                                "modifier": "log1p",
                                "factor": 0.1,
                                "missing": 0,
                            }},

                                {
                                    "weight":0,
                                    "filter":{
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

                        "from":str(page),
                        "size":20,
                        "min_score":5
                }
                resp = client.search(index='paper',body=body)
                return JsonResponse(resp['hits'])
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'errno':'1'})

    def search_by_id_list(idList):
        body = {
            "query": {
                "terms": {
                    "id": idList
                }
            }
        }
        resp = client.search(index='paper', body=body)
        hits = resp['hits']['hits']
        return hits
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
                            vlist.append(hit['_source']['venue']['raw'])
                return JsonResponse({'data': vlist})
            else:
                return JsonResponse({'errno': '1'})
        except Exception as e:
            traceback.print_exc()

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
                            klist.append(k.strip())
                return JsonResponse({'data': klist})
            else:
                return JsonResponse({'errno': '1'})
        except Exception as e:
            traceback.print_exc()

    def getOrgListByIdList(request):
        try:
            if request.method == 'POST':
                para = eval(request.body)
                idList = para['idList']
                hits = publication.search_by_id_list(idList)
                olist = []
                for hit in hits:
                    for a in hit['_source']['authors']:
                        if('org' in a):
                            list = a['org'].split(',')
                            for i in list:
                                if('University' in i or 'Université' in i or '大学' in i):
                                    olist.append(i.strip())
                return JsonResponse({'data':olist})
            else:
                return JsonResponse({'errno': '1'})
        except Exception as e:
            traceback.print_exc()