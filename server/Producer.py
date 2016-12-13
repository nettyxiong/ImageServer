# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

from util import MapFileUtil
from util import RedisUtil
from util import HbaseUtil
from util import HdfsUtil
from util import FileUtil

import pickle
from os.path import join
from hadoop.io.IntWritable import LongWritable
from hadoop.io import MapFile
from hadoop.io import Text

import random
import logging
logging.basicConfig(
	level=logging.INFO,
	format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
	datefmt='%Y-%m-%d %H:%M:%S',   
)
MAX_MAPFILE_ID = 1000000
class MapFileProducer:
	def __init__(self,images,settings):
		self.images = images
		self.mapFileId = '1'
		self.settings = settings
	
	def _generateMapFileId(self):
		while True:
			self.mapFileId = str(random.randint(1,MAX_MAPFILE_ID))
			if not FileUtil.exists(self.mapFileId):
				break

	def _createMapFile(self):
		self._generateMapFileId()
		return MapFileUtil.createMapFile(self.images,self.mapFileId)

	def _writeToHDFS(self):
		return HdfsUtil.write(self.mapFileId,self.settings.images_hdfs_path)

	def _addRecord(self,db="hbase"):
		data = {}
		for imageId in self.images:
				data[imageId] = self.mapFileId
		if db.lower() == "hbase":
			return HbaseUtil.put(data)
		elif db.lower() == "redis":
			return RedisUtil.hmsetImageToMapfile(data)
		else:
			logging.error("db type error,only can choose 'hbase' or 'redis' now")
			return False
	
	def run(self):
		if self._createMapFile():
			if self._writeToHDFS() and self._addRecord():
				if FileUtil.removeFolder(self.mapFileId):
					return True
		else:
			logging.error("fail to produce mapfile")
			return False

from configs import settings
if __name__ == '__main__':
	producer = MapFileProducer(["Video_8582-frame29.jpg"],settings)
	if producer.run():
		logging.info("produce a mapfile success")