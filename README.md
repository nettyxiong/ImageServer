# ImageServer 
基于HBASE的图片存储服务
# 版本二
1. 参考Quora上的帖子[Is-it-possible-to-use-HDFS-HBase-to-serve-images](https://www.quora.com/Is-it-possible-to-use-HDFS-HBase-to-serve-images)
2. 图片以二进制形式存储于HBASE中
3. 依赖 python 2.7+
4. `sudo pip install -U -r requirements.txt`

### api.py
###### 图片REST API
1. GET /api/image/imageId 获取imageId的图片
2. DEL /api/image/imageId 删除imageId的图片
3. PUT /api/image/imageId 上传imageId的图片
4. POST /api/image/imageId 更新imageId的图片
5. POST /api/images/ 上传多张图片
###### 运行
```bash
gunicorn -c gunicorn_config.py api:app
or
python api.py 
```
### client.py
- 上传图片，支持文件夹与单张图片两种方式
- example
```bash
python client.py ~/Pictures/Video_8582/frame29.jpg
or
python client.py ~/Pictures/Video_8582
```
### benchmark
1. 依赖[Multi-Mechanize](http://multi-mechanize.readthedocs.io/en/latest/index.html)
2. multimech-run benchmark
3. 结果在 benchmark/results下，打开其中html文件即可展示
4. 同时观察磁盘、网络IO、CPU等资源消耗情况

    - glances
    - iostat -d -x -k 1
  
5. 测试结果

        Request TYPE | tps | 瓶颈
        ----|------|----
        GET | 1200  | 磁盘IO
        POST | 1100  | 磁盘IO
        
        [GET](http://htmlpreview.github.io/?https://github.com/sixiong/ImageServer/blob/v2/benchmark/results/results_2016.12.07_16.38.10/results.html)

        [POST](http://htmlpreview.github.io/?https://github.com/sixiong/ImageServer/blob/v2/benchmark/results/results_2016.12.08_10.08.11/results.html)
6. 原因分析

整个HBASE集群搭建在docker中，所有节点的磁盘IO都是经由宿主机来完成的，故磁盘IO很容易跑满，成为瓶颈</br>
以上可以解释POST测试结果图中突然下降的原因

### restart-cluster.sh
- 基于docker部署hbase、hdfs
- 自行保证有hbase、hdfs集群即可
- 在settings.py中进行相关参数配置
