FROM alpine:latest

# instalăm python + cron + docker-cli + bash + dos2unix
RUN apk add --no-cache python3 py3-pip curl bash busybox-suid docker-cli dos2unix

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
