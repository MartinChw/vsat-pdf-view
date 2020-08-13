FROM python:3.7-buster
USER root
ENV TZ=Asia/Shanghai
ENV LANG C.UTF-8
WORKDIR /app
COPY . /app/backend
RUN pip3 install -r requirements.txt -i "https://pypi.doubanio.com/simple/"
CMD python3 run.py