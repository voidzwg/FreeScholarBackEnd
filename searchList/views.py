from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.generic import View
from .models import Comment, Collection


class PaperData(View):
    def post(self, request, *args, **kwargs):
        uid = request.POST.get('u_id')
        paper = request.POST.get('p_id')
        comments = Comment.objects.filter(paper_id=paper)
        user_collected = False
        comment_num = comments.__len__()
        collections = Collection.objects.filter(paper_id=paper)
        for collection in collections:
            if str(collection.user.field_id) == uid:
                user_collected = True

        collection_num = collections.__len__()
        json_data = {
            'user_collected': user_collected,
            'collection_num': collection_num,
            'comment_num': comment_num
        }
        return JsonResponse(json_data, safe=False)

