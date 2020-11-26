# Развертывание серверов Redis и создание из них кластера


## Создание контейнеров:

Первым делом необходимо перейти в папку **servers_redis** выполнив команду 
```bash
cd servers_redis
```


Необходимо выполнить команды, приведенные ниже, при этом при создании ***redis_control*** необходимо указывать ip-адреса серверов

```bash
docker run -dt -v $PWD/c_replic.conf:/usr/local/etc/redis/c_replic.conf --net=host --name redis_server_cr redis redis-server /usr/local/etc/redis/c_replic.conf
docker run -dt -v $PWD/b_replic.conf:/usr/local/etc/redis/b_replic.conf --net=host --name redis_server_br redis redis-server /usr/local/etc/redis/b_replic.conf
docker run -dt -v $PWD/a_replic.conf:/usr/local/etc/redis/a_replic.conf --net=host --name redis_server_ar redis redis-server /usr/local/etc/redis/a_replic.conf
docker run -dt -v $PWD/c_master.conf:/usr/local/etc/redis/c_master.conf --net=host --name redis_server_c redis redis-server /usr/local/etc/redis/c_master.conf
docker run -dt -v $PWD/b_master.conf:/usr/local/etc/redis/b_master.conf --net=host --name redis_server_b redis redis-server /usr/local/etc/redis/b_master.conf
docker run -dt -v $PWD/a_master.conf:/usr/local/etc/redis/a_master.conf --net=host --name redis_server_a redis redis-server /usr/local/etc/redis/a_master.conf
docker run -dt --name redis_control redis redis-cli --cluster create 194.61.2.84:6379 194.61.2.84:6380 194.61.2.84:6381 194.61.2.84:6382 194.61.2.84:6383 194.61.2.84:6384 --cluster-replicas 1 --verbose --cluster-yes
docker ps -a
```

## Удаление контейнеров:

Когда контейнеры больше не нужны можно их все убрать, выполнив команды, приведенные ниже: 

```bash
docker stop redis_control
docker stop redis_server_a
docker stop redis_server_b
docker stop redis_server_c
docker stop redis_server_ar
docker stop redis_server_br
docker stop redis_server_cr
docker rm redis_control
docker rm redis_server_a
docker rm redis_server_b
docker rm redis_server_c
docker rm redis_server_ar
docker rm redis_server_br
docker rm redis_server_cr
docker ps -a
```

Хотя правильнее было бы остановить работу кластера, а уж потом удалять все контейнеры, но этот метод тоже работает `¯\_(ツ)_/¯`.


