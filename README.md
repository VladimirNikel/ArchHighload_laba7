# Архитектура высоконагруженных система. ДЗ №7
## Два сервиса на разных языках программирования


## Цель:
> Взять сервер из 1-го ДЗ и:
> 1. Создать ручку PUT/POST для сохранения погоды на сервер.
> 2. Настроить сохранение всех данных о погоде в redis.
> 3. Исправить ручку GET так, чтобы проверка данных проходила через redis. Если данных в redis нет, то их необходимо запросить у сервиса-источника погоды, сохранить в redis и отдать пользователю.
> 4. Нужно настроить репликацию и шардирование для redis. Должно быть как минимум два шарда redis.
> * можно использовать *Redis Cluster* или *Redis/Sentinel/temproxy* или *mcrouter/memcahed*
> * проверить отказоустойчивость при падении мастера, наличие равномерного шардирования

--------------


**Шардирование** - метод разделения и хранения единого логического набора данных в виде множества баз данных. Другое определение шардинга — горизонтальное разделение данных.


--------------

## Инструкция по установке:
1. Скачать/стянуть репозиторий
1. Перейти в папку репозитория
1. На сервере, где будут находиться контейнеры Redis'а выполнить команды для запуска контейнеров:
	- либо перейти в репозитории в папку `servers_redis` и выполнить всё по инструкции в [README.md](https://github.com/VladimirNikel/ArchHighload_laba7/blob/master/servers_redis/README.md)
	- либо выполнить набор команд:
	```bash
	docker run -dt -v servers_redis/c_replic.conf:/usr/local/etc/redis/c_replic.conf --net=host --name redis_server_cr redis redis-server /usr/local/etc/redis/c_replic.conf
	docker run -dt -v servers_redis/b_replic.conf:/usr/local/etc/redis/b_replic.conf --net=host --name redis_server_br redis redis-server /usr/local/etc/redis/b_replic.conf
	docker run -dt -v $servers_redis/a_replic.conf:/usr/local/etc/redis/a_replic.conf --net=host --name redis_server_ar redis redis-server /usr/local/etc/redis/a_replic.conf
	docker run -dt -v servers_redis/c_master.conf:/usr/local/etc/redis/c_master.conf --net=host --name redis_server_c redis redis-server /usr/local/etc/redis/c_master.conf
	docker run -dt -v servers_redis/b_master.conf:/usr/local/etc/redis/b_master.conf --net=host --name redis_server_b redis redis-server /usr/local/etc/redis/b_master.conf
	docker run -dt -v servers_redis/a_master.conf:/usr/local/etc/redis/a_master.conf --net=host --name redis_server_a redis redis-server /usr/local/etc/redis/a_master.conf
	docker run -dt --name redis_control redis redis-cli --cluster create 194.61.2.84:6379 194.61.2.84:6380 194.61.2.84:6381 194.61.2.84:6382 194.61.2.84:6383 194.61.2.84:6384 --cluster-replicas 1 --verbose --cluster-yes
	docker ps -a
	```
1. На сервере/серверах:
    1. Выполнить команду `docker build -t <название образа> -f dockerfile . `, мною для работы используется исходный образ ubuntu. Поэтому для создания образов использую команды:
    	```bash
		docker build -t ubuntu/archhightload_laba7_1 -f dockerfile1 .
		docker build -t ubuntu/archhightload_laba7_2 -f dockerfile2 .
    	```
    1. Выполнить команду `docker run -it --name <название контейнера> -p 0.0.0.0:<порт>:8000 ubuntu/archhightload_laba7` для создания docker-контейнера из docker-образа. В рамках задания были выполнены команды:
    	```bash
		docker run -dt --name laba7_1_archHL -p 0.0.0.0:5020:8000 ubuntu/archhightload_laba7_1
		docker run -dt --name laba7_2_archHL -p 0.0.0.0:5030:8000 ubuntu/archhightload_laba7_2
        ```
1. Пользоваться приложением:
	- либо браузером по [адресу](http://127.0.0.1:80) 
	- либо терминалом:
	  - `curl http://127.0.0.1:80/v1/current/?city=Moscow` - чтобы узнать текущую температуру в городе Moscow (можно использовать и другие города, хы)
      - `curl "http://127.0.0.1:80/v1/forecast/?city=Moscow&timestamp=3h"` - чтобы узнать прогноз погоды в интересующем Вас городе и используя *timestamp*:
        * `1h` - чтобы увидеть прогноз погоды на 1 час вперед
        * `3h` - чтобы увидеть прогноз погоды на 3 часа вперед

## Инструментарий:
- GIT (устанавливается командой `sudo apt install git -y`)
- Установленные модули:
	+ FastAPI `sudo pip3 install fastapi`
	+ Unicorn `sudo pip3 install uvicorn`
	+ redis-py-cluster `sudo pip3 install redis-py-cluster` [ссылка](https://pypi.org/project/redis-py-cluster/)
	+ ~~ранее был использован ***redis***, но он [не поддерживает работу с кластером](https://github.com/andymccurdy/redis-py#cluster-mode)~~
