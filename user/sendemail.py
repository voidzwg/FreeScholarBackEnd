import os
from random import Random

from django.core.mail import send_mail

from user.models import EmailCode
import re

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'


def random_str(randomlength=6):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def sendCodeEmail(email):
    emailCode = EmailCode.objects.filter()
    emailCode.delete()
    code = random_str(6)

    newCode = EmailCode()
    newCode.emailcode = code
    newCode.save()

    email_title = "Free-Scholar系统邮箱验证码"
    email_body = "欢迎来到Free-Scholar系统!\n"
    email_body += "您的认领门户申请邮箱验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证.\n".format(code)
    email_body += "如果您从未认领门户申请,请忽略该邮件."

    send_status = send_mail(email_title, email_body, '810607510@qq.com', [email])
    return send_status


def CheckCode(code):
    if not EmailCode.objects.filter(code=code).exists():
        return False
    else:
        EmailCode.objects.filter(code=code).delete()
        return True

def validate_email(code):
    # pattern = re.compile(r'[\w\.]*@[a-zA-Z0-9]+\.[com|.gov|.net]')
    pattern = re.compile(r'(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)')
    result = pattern.match(code)
    if result:
        return True
    else:
        return False