# Create your views here.
from django.http import JsonResponse
from django.views.generic import View

from .models import Scholarportal


class GetBaseInfo(View):
    model = Scholarportal

    def get(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        portal = self.model.objects.get(field_id=pid)
        scholar = portal.scholar
        user = scholar.user
        json_data = {
            "introduction": user.bio,
            "userName": user.name,
            "userMajor": scholar.field,
            "visitors": portal.count,
            "heat": scholar.hot_index,
            "institution": scholar.affi,
            "Hotpoint":portal.count*347+443*(portal+1)+666
        }
        return JsonResponse(json_data, safe=False)
