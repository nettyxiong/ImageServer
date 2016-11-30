
sudo docker stop some-redis
sudo docker stop hadoop-master
sudo docker stop hadoop-slave1
sudo docker stop hadoop-slave2
sudo docker stop hadoop-slave3

sudo docker start hadoop-slave1
sudo docker start hadoop-slave2
sudo docker start hadoop-slave3
sudo docker start hadoop-master
sudo docker start some-redis

sudo docker exec -it hadoop-master bash


