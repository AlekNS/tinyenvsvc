FROM mhart/alpine-node:11 as builder

WORKDIR /home/frontend

COPY . .
RUN npm i && npm run build:prod


FROM nginx:1.14-alpine

WORKDIR /usr/www
ENV ENV_FILE=.env

COPY scripts/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /home/frontend/dist dist

RUN mkdir -p /run/nginx

ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]

EXPOSE 18080
EXPOSE 18443
