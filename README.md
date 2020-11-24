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
1. На сервере (а лучше в контейнере) выполнить установку redis при помощи следующих команд:
```bash
apt install make

redisurl="http://download.redis.io/redis-stable.tar.gz"
curl -s -o redis-stable.tar.gz $redisurl
mkdir -p /usr/local/lib/
chmod a+w /usr/local/lib/
tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd /usr/local/lib/redis-stable/
make && make install								#какая-то ошибка тут

ls -hFG /usr/local/bin/redis-* | sort
/usr/local/bin/redis-benchmark*
/usr/local/bin/redis-check-aof*
/usr/local/bin/redis-check-rdb*
/usr/local/bin/redis-cli*
/usr/local/bin/redis-sentinel@
/usr/local/bin/redis-server*

mkdir -p /etc/redis/
touch /etc/redis/6379.conf
# /etc/redis/6379.conf
 
echo "port              6379" > /etc/redis/6379.conf
echo "daemonize         yes" >> /etc/redis/6379.conf
echo "save              60 1" >> /etc/redis/6379.conf
echo "bind              127.0.0.1" >> /etc/redis/6379.conf
echo "tcp-keepalive     300" >> /etc/redis/6379.conf
echo "dbfilename        dump.rdb" >> /etc/redis/6379.conf
echo "dir               ./" >> /etc/redis/6379.conf
echo "rdbcompression    yes" >> /etc/redis/6379.conf


redis-server /etc/redis/6379.conf #Запуск самого сервера
```



## Инструментарий:
- GIT (устанавливается командой `sudo apt install git -y`)
- Установленные модули:
	+ FastAPI `sudo pip3 install fastapi`
	+ Unicorn `sudo pip3 install uvicorn`
	+ Redis `sudo pip3 install redis`

