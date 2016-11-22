# ImageServer 
基于HDFS的图片存储服务
# 版本一
1. 参考博客[hadoop+hbase海量图片存储](http://blog.csdn.net/good_mpj/article/details/43309553?ref=myread)
2. 图片以MapFile形式存储于HDFS中
3. 构建MapFile生成队列，当队列达到阈值后，构建MapFile,写入HDFS中
4. 队列使用Redis，元数据存储于Redis，图像数据暂存于localFileSystem
5. 构建MapFileId与图片Id之间的对应关系，此K-V键值对存储于HBase/Redis

### server
1. 队列监测端，常驻内存服务，队列满启动创造MapFile写Hdfs流程
2. 安装:`cd server && sudo pip install -r requirements.txt`
3. 运行：`nohup python server.py > server.out &`

### client
1. 写入图片到server的预备队列，支持批量写入
2. 安装:`cd client && sudo pip install -r requirements.txt`
3. 运行:`python client.py "~/Picetures"` or `python client.py "~/Picetures/frame10.jpg"`



