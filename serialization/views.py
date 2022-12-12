# Create your views here.
from django.http import JsonResponse
from django.views import View


class Serialization(View):
    model = None
    slist = None

    def post(self, request, *args, **kwargs):
        field_id = request.POST.get('field_id')
        if self.model is None or self.slist is None:
            return JsonResponse({'errno': -1, 'msg': "参数错误"})
        try:
            obj = self.model.objects.get(field_id=field_id)
        except self.model.DoesNotExist:
            return JsonResponse({'errno': -2, 'msg': "序列化对象不存在"})
        json_data = {}
        for s in self.slist:
            json_data[s] = obj.serializable_value(s)
        return JsonResponse(json_data)
