# Create your views here.
import datetime

from django.http import JsonResponse
from django.views import View

from utils.Token import Authentication
from utils.media import *


class Media(View):
    post_type = 0
    model = None

    def upload_img(self, field_id, img, url):
        try:
            obj = self.model.objects.get(field_id=field_id)
        except self.model.DoesNotExist as e:
            print(e)
            return None
        img_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f_') + str(field_id) + '_' + img.name
        try:
            obj.avatar = img_name
            obj.save()
        except Exception as e:
            print(e)
            return {'errno': -4, 'msg': "模型不存在对应属性"}
        f = open(os.path.join(MEDIA_ROOT, url, img_name), 'wb')
        for i in img.chunks():
            f.write(i)
        f.close()
        return {'errno': 0, 'msg': "上传成功"}

    def post(self, request, *args, **kwargs):
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        uid = payload.get('id')
        img = request.POST.get('img')
        if img is None or img == '':
            return JsonResponse({'errno': -1, 'msg': "图片不能为空"})
        if not img.name.lower().endswith(IMAGE_TAIL):
            return JsonResponse({'errno': -2, 'msg': "文件格式错误"})
        if self.model is None:
            return JsonResponse({'errno': -6, 'msg': "illegal model"})
        if self.post_type == 1:
            ret = self.upload_img(uid, img, 'avatars')
            if ret is None:
                return JsonResponse({'errno': -3, 'msg': "用户不存在"})
            return JsonResponse(ret)
        elif self.post_type == 2:
            fid = request.POST.get('fid')
            ret = self.upload_img(fid, img, 'coverimgs')
            if ret is None:
                return JsonResponse({'errno': -3, 'msg': "收藏夹不存在"})
            return JsonResponse(ret)
        else:
            return JsonResponse({'errno': -5, 'msg': "illegal post type"})

