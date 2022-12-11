# Create your views here.
import datetime

from django.http import JsonResponse
from django.views.generic import View

from utils.Token import Authentication
from .models import Message, User
from utils.superuser import SUPERUSER


def message_serialize(message_list, sender=True):
    system_message_list = []
    user_message_list = []
    full_message_list = []
    for message in message_list:
        if sender:
            user = message.sender
        else:
            user = message.owner
        json_data = {
            'mid': message.field_id,
            'username': user.name,
            'avatar': user.avatar,
            'content': message.content,
            'create_time': message.create_time,
            'is_read': message.is_read
        }
        if sender:
            json_data['sender_id'] = message.sender_id
        else:
            json_data['owner_id'] = message.owner_id
        full_message_list.append(json_data)
        if message.sender.field_id in SUPERUSER:
            system_message_list.append(json_data)
        else:
            user_message_list.append(json_data)
    return system_message_list, user_message_list, full_message_list


class MessageCenter(View):
    model = Message
    get_type = post_type = 0

    def get(self, request, *args, **kwargs):
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        uid = payload.get('id')
        if self.get_type == 1 or self.get_type == 2:
            message_list = Message.objects.filter(owner_id=uid)
            system_message_list, user_message_list, full_message_list = message_serialize(message_list)
            if self.get_type == 1:
                return JsonResponse(system_message_list, safe=False)
            else:
                return JsonResponse(user_message_list, safe=False)
        elif self.get_type == 3:
            message_list = Message.objects.filter(sender_id=uid)
            system_message_list, user_message_list, full_message_list = message_serialize(message_list, sender=False)
            return JsonResponse(full_message_list, safe=False)
        else:
            return JsonResponse({'errno': 2, 'msg': "illegal get_type"})

    def post(self, request, *args, **kwargs):
        fail, payload = Authentication.authentication(request.META)
        if fail:
            return JsonResponse(payload)
        if self.post_type != 3:
            mid = request.POST.get('mid')
            try:
                message = self.model.objects.get(field_id=mid)
            except Message.DoesNotExist:
                return JsonResponse({'errno': 1, 'msg': "message不存在"})
            if self.post_type == 1:
                message.delete()
            elif self.post_type == 2:
                message.is_read = True
                message.save()
            else:
                return JsonResponse({'errno': 2, 'msg': "illegal post_type"})
        else:
            owner_id = request.POST.get('owner_id')
            content = request.POST.get('content')
            sender_id = payload.get('id')
            create_time = datetime.datetime.now()
            msg = Message(owner_id=owner_id, sender_id=sender_id, content=content,
                          create_time=create_time, is_read=False)
            msg.save()
        return JsonResponse({'errno': 0, 'msg': 'success'})
