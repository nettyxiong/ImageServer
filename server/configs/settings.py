import os
#image folder path
prepare_dir="/home/sxiong/workspace/image-queue-py/images/preImages"
queue_dir="/home/sxiong/workspace/image-queue-py/images/queueImages"
images_hdfs_path="hdfs://172.19.0.2:9000/images"

#scp config
server_host="127.0.0.1"
ssh2_port=22
ssh2_username="sxiong"
ssh2_passwd="123456"

#redis config
redis_host="127.0.0.1"
redis_port=6379
redis_db=1

#Hbase config
hbase_host="172.17.0.5"
hbase_table_prefix="imageserver"
hbase_table_name="mapfileid_imageid"

#Byte
MAX_IMAGE_SIZE=200

#time interval
TIME_INTERVAL=3


