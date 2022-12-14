from django.shortcuts import render
from django.http import JsonResponse
import traceback
# Create your views here.
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from utils.Token import Authentication
from publication.models import *
import sys, io
from publication import *
from FreeScholarBackEnd.settings import *

class author:

    def getAuthor(request):
        try:
            if request.method == 'POST':
                id= request.POST.get('id')
                body = {
                    "query":{
                        "term":{
                            "id":id
                        }
                    }
                }
                resp = client.search(index='author', body=body)
                if resp['hits']['total']['value'] != 0:
                    data = resp['hits']['hits'][0]['_source']
                    list = []
                    pubs = data['pubs']
                    for p in pubs:
                        list.append(p['i'])
                    body = {
                        "query": {
                            "terms": {
                                "id": list
                            }
                        }
                    }
                    resp = client.search(index='paper', body=body)
                    pubs = []
                    for h in resp['hits']['hits']:
                        pubs.append(h['_source'])
                    data['pubs'] = pubs
                    authors = []
                    # for p in pubs:
                    #      for a in p['authors']:
                    #          if a['name'] in authors:
                    #              authors[a['name']]+=1
                    #          else:
                    #              authors[a['name']]=1
                    for p in pubs:
                        for a in p['authors']:
                            flag = False
                            for j in authors:
                                if a['name'] == j['name']:
                                    flag = True
                                    break
                            if flag:
                                continue
                            if 'id' in a:
                                if a['id'] == id:
                                    continue
                                body = {
                                    "query": {
                                        "bool":{
                                            'filter':[
                                                {"term": {
                                                    "authors.id": id
                                                }},

                                                {"term": {
                                                    "authors.id": a['id']
                                                }}
                                            ]
                                        }
                                    }
                                }
                                count = client.count(index='paper',body=body)
                                item = {
                                    'id':a['id'],
                                    'name':a['name'],
                                    'count':count['count']
                                }
                                authors.append(item)
                            else:
                                if a['name'] == data['name']:
                                    continue
                                body = {
                                    "query": {
                                        "bool":{
                                            'filter': [
                                                {"term": {
                                                    "authors.id": id
                                                }},

                                                {"term": {
                                                    "authors.name.keyword": a['name']
                                                }}
                                            ]
                                        }
                                    }
                                }
                                count = client.count(index='paper', body=body)
                                item = {
                                    'name': a['name'],
                                    'count':count['count'],
                                }
                                authors.append(item)
                    return JsonResponse({'data':data,'coworkers':authors})

                else:
                    return JsonResponse({'err':2,'msg':'查无此人'})
            else:
                return JsonResponse({'err':'1','msg':'request method error! post expected.'})
        except Exception as e:
            traceback.print_exc()

    def search(request):
        if request.method == 'POST':
            try:
                name= request.POST.get('name')

            except Exception as e:
                traceback.print_exc()
        else:
            return JsonResponse({'err': '1', 'msg': 'request method error! post expected.'})