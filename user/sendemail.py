import os
from random import Random

from django.core.mail import send_mail

from user.models import EmailCode
import re
from django_redis import get_redis_connection

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

email_connection = get_redis_connection()
expire = 60
email_connection.expire('email', expire)


def random_str(randomlength=6):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def sendCodeEmail(email, id):
    code = random_str(6)
    email_connection.zadd("email",{code: id})

    email_title = "Free-Scholar系统邮箱验证码"
    email_body = "欢迎来到Free-Scholar系统!\n"
    email_body += "您的认领门户申请邮箱验证码为：{0}, 该验证码有效时间为一分钟，请及时进行验证.\n".format(code)
    email_body += "如果您从未认领门户申请,请忽略该邮件."

    send_status = send_mail(email_title, email_body, '810607510@qq.com', [email])
    return send_status


def CheckCode(code, id):
    print(code)

    code_1=email_connection.zrangebyscore("email",id,id)
    code_2=code_1[0].decode()
    print(code_2)
    if code_2 != code:
        return False
    else:
        return True


def validate_email(code):
    # pattern = re.compile(r'[\w\.]*@[a-zA-Z0-9]+\.[com|.gov|.net]')
    pattern = re.compile(r'(^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$)')
    result = pattern.match(code)
    if result:
        return True
    else:
        return False
