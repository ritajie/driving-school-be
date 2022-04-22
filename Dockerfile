# $ docker run -d -p 1234:1234 --name car_be {image}

FROM rackspacedot/python37

LABEL maintainer="1551755561@qq.com"

COPY ./requirements.txt /requirements.txt
COPY ./.bashrc /root/.bashrc

RUN apt update
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 1234

COPY . /root/driving-school-be/

WORKDIR /root/driving-school-be/

ENV IS_PRODUCTION 1

CMD ["/bin/bash", "bin/gunicorn_start.sh"]
