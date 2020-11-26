FROM redis:5.0

ARG PORT_CONFIG

COPY servers_redis/a_master.conf /usr/local/etc/redis/redis.conf

RUN sed -i "s/6379/${PORT_CONFIG}/g" "/usr/local/etc/redis/redis.conf"

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
