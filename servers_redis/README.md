# Развертывание серверов/кластеров Redis

[1 источник знаний](https://medium.com/commencis/creating-redis-cluster-using-docker-67f65545796d)

[2 источник знаний](https://redis.io/topics/cluster-tutorial)

[3 источник знаний](https://netpoint-dc.com/blog/redis-cluster-linux/)

1. Потребуются все файлы из этой директории на той машине/машинах, где будет развернуты в docker-контейнерах сервера redis'а

1. Создадим отдельную сеть для контейнеров (так надо)
	```
	docker network create cluster_redis
	```
	> С этой штукой контейнеры сразу умирают... Пока делать не советую

1. По желанию можете удостовериться в том, что сеть создана, выполнением команды
	```
	docker network ls
	```

1. Далее, создайте (либо скопируйте) файл `redis.conf`. Главное, чтобы в этом файле были следующие записи:
	```
	port 6379
	cluster-enabled yes
	cluster-config-file nodes.conf
	cluster-node-timeout 5000
	appendonly yes
	```

1. Создайте необходимое количество контейнеров следующей командой:
	```
	docker run -dt -v $PWD/redis.conf:/usr/local/etc/redis/redis.conf --name redis_server<№> --net cluster_redis redis redis-server /usr/local/etc/redis/redis.conf
	```

	Я создал 6 контейнеров:
	```
	docker run -dt -v $PWD/redis.conf:/usr/local/etc/redis/redis.conf -p 5026:6379 --name redis_server6 --net cluster_redis redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v $PWD/redis.conf:/usr/local/etc/redis/redis.conf -p 5025:6379 --name redis_server5 --net cluster_redis redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v $PWD/redis.conf:/usr/local/etc/redis/redis.conf -p 5024:6379 --name redis_server4 --net cluster_redis redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v $PWD/redis.conf:/usr/local/etc/redis/redis.conf -p 5023:6379 --name redis_server3 --net cluster_redis redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v $PWD/redis.conf:/usr/local/etc/redis/redis.conf -p 5022:6379 --name redis_server2 --net cluster_redis redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v $PWD/redis.conf:/usr/local/etc/redis/redis.conf -p 5021:6379 --name redis_server1 --net cluster_redis redis redis-server /usr/local/etc/redis/redis.conf
	```

1. Далее необходимо узнать IP-адрес каждого контейнера:
	```
	docker inspect redis_server1 | grep "IPAddress"
	docker inspect redis_server2 | grep "IPAddress"
	docker inspect redis_server3 | grep "IPAddress"
	docker inspect redis_server4 | grep "IPAddress"
	docker inspect redis_server5 | grep "IPAddress"
	docker inspect redis_server6 | grep "IPAddress"
	```

1. Далее надо создать контейнер, который будет управлять нашими контейнерами с redis
	```
	docker run -i --rm ruby sh -c '\
	gem install redis \
	&& wget http://download.redis.io/redis-stable/src/redis-trib.rb \
	&& ruby ./redis-trib.rb create --replicas 1 172.17.0.8:6379 172.17.0.9:6379 172.17.0.10:6379 172.17.0.11:6379 172.17.0.12:6379 172.17.13:6379'
	```

	Либо 

	```
	docker run -i --rm ruby sh -c '\
	gem install redis \
	&& wget http://download.redis.io/redis-stable/src/redis-trib.rb \
	&& redis-cli --cluster create 172.17.0.8:5025 172.17.0.9:5024 172.17.0.10:5023 172.17.0.11:5022 172.17.0.12:5021 172.17.13:5026 --cluster-replicas 1'
	```




	```
	docker run -dt --name redis_control redis redis-cli -h 172.17.0.12 -p 5021 --cluster create 172.17.0.8:5025 172.17.0.9:5024 172.17.0.10:5023 172.17.0.11:5022 172.17.0.12:5021 172.17.13:5026 --cluster-replicas 1
	```


	но ничего из приведенного не дает результата



	Чем я баловался: ~~(не работает так)~~
	```bash
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf --net=host --name redis_server6 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf --net=host --name redis_server5 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf --net=host --name redis_server4 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf --net=host --name redis_server3 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf --net=host --name redis_server2 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf --net=host --name redis_server1 redis redis-server /usr/local/etc/redis/redis.conf
	```

	Удаление контейнеров:
	```bash
	docker stop redis_server1
	docker stop redis_server2
	docker stop redis_server3
	docker stop redis_server4
	docker stop redis_server5
	docker stop redis_server6
	docker rm redis_server1
	docker rm redis_server2
	docker rm redis_server3
	docker rm redis_server4
	docker rm redis_server5
	docker rm redis_server6
	docker ps -a
	```

	создание контейнеров:
	```bash
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf -p 5026:6379 -p 15026:16379 --name redis_server6 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf -p 5025:6379 -p 15025:16379 --name redis_server5 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf -p 5024:6379 -p 15024:16379 --name redis_server4 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf -p 5023:6379 -p 15023:16379 --name redis_server3 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf -p 5022:6379 -p 15022:16379 --name redis_server2 redis redis-server /usr/local/etc/redis/redis.conf
	docker run -dt -v redis.conf:/usr/local/etc/redis/redis.conf -p 5021:6379 -p 15021:16379 --name redis_server1 redis redis-server /usr/local/etc/redis/redis.conf
	docker ps -a
	```


```
redis-cli --cluster create 0.0.0.0:5021 0.0.0.0:5022 0.0.0.0:5023 0.0.0.0:5024 0.0.0.0:5025 0.0.0.0:5026 --cluster-replicas 1
```



-----------

# попытка №2

либо пользуемся ***redis*** - образом docker'а, либо формируем свой образ (на той же ubuntu либо другой ОС на ваш вкус)
- образ docker'a:
	```
	from redis
	...
	```

- свой образ на основе любой ос
	нам потребуются минимальные компоненты:

	```
	sudo apt-get update && sudo apt-get upgrade
	sudo apt install make gcc libc6-dev tcl
	```

	далее выполняем команды:

	```
	wget http://download.redis.io/redis-stable.tar.gz
	tar xvzf redis-stable.tar.gz
	cd redis-stable
	sudo make install
	```

	и тестим `make test`

	в докерах не потребуется использование `sudo`, а вот на реальных машинах - потребуется.




```
docker run -i --rm ruby sh -c '\
gem install redis \
&& wget http://download.redis.io/redis-stable/src/redis-trib.rb \
&& chmod +x ./redis-trib.rb \
&& ./redis-trib.rb create 172.17.0.8:5021 172.17.0.9:5022 172.17.0.10:5023'
```

-----------

# попытка №3


	создание контейнеров:
	```bash
	docker run -dt -v redis-5033_replica.conf:/usr/local/etc/redis/redis-5033_replica.conf -p 5026:6379 -p 15026:16379 --name redis_server6 redis redis-server /usr/local/etc/redis/redis-5033_replica.conf
	docker run -dt -v redis-5032_replica.conf:/usr/local/etc/redis/redis-5032_replica.conf -p 5025:6379 -p 15025:16379 --name redis_server5 redis redis-server /usr/local/etc/redis/redis-5032_replica.conf
	docker run -dt -v redis-5031_replica.conf:/usr/local/etc/redis/redis-5031_replica.conf -p 5024:6379 -p 15024:16379 --name redis_server4 redis redis-server /usr/local/etc/redis/redis-5031_replica.conf
	docker run -dt -v redis-5023_master.conf:/usr/local/etc/redis/redis-5023_master.conf -p 5023:6379 -p 15023:16379 --name redis_server3 redis redis-server /usr/local/etc/redis/redis-5023_master.conf
	docker run -dt -v redis-5022_master.conf:/usr/local/etc/redis/redis-5022_master.conf -p 5022:6379 -p 15022:16379 --name redis_server2 redis redis-server /usr/local/etc/redis/redis-5022_master.conf
	docker run -dt -v redis-5021_master.conf:/usr/local/etc/redis/redis-5021_master.conf -p 5021:6379 -p 15021:16379 --name redis_server1 redis redis-server /usr/local/etc/redis/redis-5021_master.conf
	docker ps -a
	```

	Удаление контейнеров:
	```bash
	docker stop redis_server1
	docker stop redis_server2
	docker stop redis_server3
	docker stop redis_server4
	docker stop redis_server5
	docker stop redis_server6
	docker rm redis_server1
	docker rm redis_server2
	docker rm redis_server3
	docker rm redis_server4
	docker rm redis_server5
	docker rm redis_server6
	docker ps -a
	```