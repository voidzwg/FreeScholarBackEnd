# Create your views here.
from django.http import JsonResponse
from django.views.generic import View

from utils.Token import Authentication
from .models import Comment, Collection


class PaperData(View):
    def post(self, request, *args, **kwargs):
        has_login = True
        fail, payload = Authentication.authentication(request.META)
        if fail:
            if payload.get('errno') == -2:
                has_login = False
            else:
                return JsonResponse(payload)
        pid = request.POST.get('p_id')
        json_data = {
            'collection_num': Collection.objects.filter(paper_id=pid).count(),
            'comment_num': Comment.objects.filter(paper_id=pid).count()
        }
        if has_login:
            json_data['user_collected'] = Collection.objects.filter(paper_id=pid, user_id=payload.get('id')).count() > 0
        return JsonResponse(json_data, safe=False)

