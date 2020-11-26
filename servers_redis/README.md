# Развертывание серверов Redis и создание из них кластера


## Создание контейнеров:

Первым делом необходимо перейти в папку **servers_redis** выполнив команду 
```bash
cd servers_redis
```


Необходимо выполнить команды, приведенные ниже, при этом при создании ***redis_control*** необходимо указывать ip-адреса серверов

```bash
docker run -dt -v $PWD/c_slave.conf:/usr/local/etc/redis/c_slave.conf --net=host --name redis_server_c redis redis-server /usr/local/etc/redis/c_slave.conf
docker run -dt -v $PWD/b_slave.conf:/usr/local/etc/redis/b_slave.conf --net=host --name redis_server_b redis redis-server /usr/local/etc/redis/b_slave.conf
docker run -dt -v $PWD/a_master.conf:/usr/local/etc/redis/a_master.conf --net=host --name redis_server_a redis redis-server /usr/local/etc/redis/a_master.conf
docker run -dt --name redis_control redis redis-cli --cluster create 194.61.2.84:6379 194.61.2.84:6380 194.61.2.84:6381 --cluster-yes
docker ps -a
```

## Удаление контейнеров:

Когда контейнеры больше не нужны можно их все убрать, выполнив команды, приведенные ниже: 

```bash
docker stop redis_control
docker stop redis_server_a
docker stop redis_server_b
docker stop redis_server_c
docker rm redis_control
docker rm redis_server_a
docker rm redis_server_b
docker rm redis_server_c
docker ps -a
```

Хотя правильнее было бы остановить работу кластера, а уж потом удалять все контейнеры, но этот метод тоже работает `¯\_(ツ)_/¯`.


