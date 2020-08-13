FROM node
USER root
ENV TZ=Asia/Shanghai
ENV LANG C.UTF-8
WORKDIR /app/frontend
COPY . /app/frontend
RUN npm i
CMD npm run build