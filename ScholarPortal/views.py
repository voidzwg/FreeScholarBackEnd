# Create your views here.
from django.http import JsonResponse
from django.views.generic import View
from utils.Token import Authentication
from .models import Follow


class GetBaseInfo(View):
    model = None

    def get(self, request, *args, **kwargs):
        is_login = True
        fail, payload = Authentication.authentication(request.META)
        if fail:
            is_login = False
        author_id = request.GET.get('author_id')
        if self.model is None:
            return JsonResponse({'errno': -1, 'msg': "模型错误"})
        scholar = self.model.objects.filter(author_id=author_id)
        if not scholar:
            return JsonResponse({'errno': 1, 'msg': "学者身份未认领"})
        scholar = scholar[0]
        user = scholar.user
        json_data = {
            "Hotpoint": scholar.count * 347 + 443 * (scholar.hot_index + 1) + 666,
            'scholar_id': scholar.field_id,
            'user_id': user.field_id,
            "bio": user.bio,
            "name": user.name,
            "visitors": scholar.count,
            'bgimg': scholar.avatar,
            'papers': scholar.paper_show
        }
        scholar.count += 1
        scholar.save()
        if is_login:
            uid = payload.get('id')
            follow = Follow.objects.filter(user_id=uid, scholar=scholar)
            if follow:
                json_data['followed'] = True
            else:
                json_data['followed'] = False
        return JsonResponse(json_data, safe=False)
