# ImageServer 
基于HBASE的图片存储服务
# 版本二
1. 参考Quora上的帖子[Is-it-possible-to-use-HDFS-HBase-to-serve-images](https://www.quora.com/Is-it-possible-to-use-HDFS-HBase-to-serve-images)
2. 图片以二进制形式存储于HBASE中
3. 依赖 python 2.7+
4. `sudo pip install -r requirements.txt`

### api.py
###### 图片REST API
1. GET /api/image/imageId 获取imageId的图片
2. DEL /api/image/imageId 删除imageId的图片
3. PUT /api/image/imageId 上传imageId的图片
4. POST /api/image/imageId 更新imageId的图片
5. POST /api/images/ 上传多张图片
  
### client.py
- 上传图片，支持文件夹与单张图片两种方式
- example
```bash
python client.py ~/Pictures/Video_8582/frame29.jpg
or
python client.py ~/Pictures/Video_8582
```

### restart-cluster.sh
- 基于docker部署hbase、hdfs
- 自行保证有hbase、hdfs集群即可
- 在settings.py中进行相关参数配置
