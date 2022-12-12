# Create your views here.
import datetime

from django.http import JsonResponse
from django.views import View

from utils.Token import Authentication
from utils.media import *


class Media(View):
    post_type = 0
    model = None

    def upload_img(self, field_id, img, url, obj_name, uid=None, check_owner=False):
        try:
            obj = self.model.objects.get(field_id=field_id)
        except self.model.DoesNotExist as e:
            print(e)
            return {'errno': -3, 'msg': "模型不存在"}
        if check_owner:
            try:
                if obj.user_id != uid:
                    return {'errno': -7, 'msg': "无权限"}
            except Exception as e:
                print(e)
                return {'errno': -4, 'msg': "模型不存在对应属性"}
        img_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f_') + str(field_id) + '_' + img.name
        try:
            if hasattr(obj, obj_name):
                setattr(obj, obj_name, img_name)
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
        img = request.FILES.get('img')
        if img is None or img == '':
            return JsonResponse({'errno': -1, 'msg': "图片不能为空"})
        if not img.name.lower().endswith(IMAGE_TAIL):
            return JsonResponse({'errno': -2, 'msg': "文件格式错误"})
        if self.model is None:
            return JsonResponse({'errno': -6, 'msg': "illegal model"})
        if self.post_type == 1:
            ret = self.upload_img(uid, img, 'avatars', 'avatar')
            return JsonResponse(ret)
        elif self.post_type == 2:
            fid = request.POST.get('fid')
            ret = self.upload_img(fid, img, 'coverimgs', 'avatar', uid=uid, check_owner=True)
            return JsonResponse(ret)
        elif self.post_type == 3:
            sid = request.POST.get('scholar_id')
            ret = self.upload_img(sid, img, 'scholarbg', 'avatar', uid=uid, check_owner=True)
            return JsonResponse(ret)
        else:
            return JsonResponse({'errno': -5, 'msg': "illegal post type"})
