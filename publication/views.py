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
                body={
                    "query":{
                        "function_score": {
                            "query":{
                                "bool": {
                                    "should":shoulds
                                }
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
                                }

                            ],
                            "boost_mode": "multiply"
                        },
                    },
                        "from":str(page),
                        "size":20,

                }
                resp = client.search(index='paper',body=body)
                return JsonResponse(resp['hits'],safe=False)
            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'errno':'1'})