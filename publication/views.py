from django.shortcuts import render
from django.http import JsonResponse
import traceback
# Create your views here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search,Q
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
client = Elasticsearch('http://139.9.134.209:9200')

def search(request):
    if request.method == 'POST':
        try:
            condition= eval(request.body)
            # output:dict数据
            list = condition['condition']
            should ={
                    "bool":
                    {
                        "must":[]
                    }
            }
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
                    shoulds.append(should)
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
                    match ={"match":{field:input}}
                    should['bool']['must'].append(match)
                elif i['type'] == 'NOR':
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
                    "bool": {
                        "should":shoulds
                    }
                },
                "from":0,
                "size":20
            }
            resp = client.search(index='paper',body=body)
            return JsonResponse(resp['hits'],safe=False)
        except Exception as e:
            traceback.print_exc()
    else:
        return JsonResponse({'errno':'1'})