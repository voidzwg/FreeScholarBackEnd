# Create your views here.
from django.http import JsonResponse
from django.views.generic import View

from .models import Message, User
from  user.views import SUPERUSER


def message_serialize(message_list):
    system_message_list = []
    user_message_list = []
    full_message_list = []
    for message in message_list:
        json_data = {
            'mid': message.field_id,
            'owner_id': message.owner.field_id,
            'sender_id': message.sender.field_id,
            'content': message.content,
            'create_time': message.create_time,
            'is_read': message.is_read
        }
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
        if self.get_type == 1 or self.get_type == 2:
            owner_id = request.GET.get('owner_id')
            try:
                owner = User.objects.get(field_id=owner_id)
            except:
                return JsonResponse({'errno': 1, 'msg': "owner不存在"})
            message_list = Message.objects.filter(owner=owner)
            system_message_list, user_message_list, full_message_list = message_serialize(message_list)
            if self.get_type == 1:
                return JsonResponse(system_message_list, safe=False)
            else:
                return JsonResponse(user_message_list, safe=False)
        elif self.get_type == 3:
            sender_id = request.GET.get('sender_id')
            try:
                sender = User.objects.get(field_id=sender_id)
            except:
                return JsonResponse({'errno': 1, 'msg': "sender不存在"})
            message_list = Message.objects.filter(sender=sender)
            system_message_list, user_message_list, full_message_list = message_serialize(message_list)
            return JsonResponse(full_message_list, safe=False)
        else:
            return JsonResponse({'errno': 2, 'msg': "illegal get_type"})

    def post(self, request, *args, **kwargs):
        mid = request.POST.get('mid')
        try:
            message = self.model.objects.get(field_id=mid)
        except:
            return JsonResponse({'errno': 1, 'msg': "message不存在"})
        if self.post_type == 1:
            message.delete()
        elif self.post_type == 2:
            message.is_read = True
            message.save()
        else:
            return JsonResponse({'errno': 2, 'msg': "illegal post_type"})
        return JsonResponse({'errno': 0, 'msg': 'success'})
