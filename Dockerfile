FROM python:3.8
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone
RUN mkdir -p /var/www/html/backend
COPY ./ /var/www/html/backend/
WORKDIR /var/www/html/backend

RUN pip install -i https://pypi.doubanio.com/simple uwsgi
RUN pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt

# Windows环境下编写的start.sh每行命令结尾有多余的\r字符，需移除
RUN sed -i 's/\r//' ./start.sh
RUN chmod +x ./start.sh