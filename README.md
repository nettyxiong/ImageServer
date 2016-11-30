# ImageServer 
基于HBASE的图片存储服务
# 版本二
1. 参考Quora上的帖子[Is-it-possible-to-use-HDFS-HBase-to-serve-images](https://www.quora.com/Is-it-possible-to-use-HDFS-HBase-to-serve-images)
2. 图片以二进制形式存储于HBASE中

### restart-cluster.sh
- 基于docker部署hbase、hdfs

### api
- 图片REST API 

### client
- 上传图片，支持文件夹与单张图片两种方式
