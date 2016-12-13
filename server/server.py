from configs import settings
from util import RedisUtil
from util import MapFileUtil
from util import ScpUtil
from util import FileUtil
from Producer import MapFileProducer
import os
import time

class Server:
	def __init__(self,prepare_dir,queue_dir):
		self.prepare_dir = prepare_dir
		self.queue_dir = queue_dir
		self.num = 100

	def _getImagesTotalSize(self,imagePaths):
		return sum(os.path.getsize(os.path.join(self.prepare_dir,path)) for path in imagePaths)

	def _transfer(self,size):
		images = RedisUtil.pop(self.num,"prepare")
		if images:
			if RedisUtil.push(images,"image") and RedisUtil.addSize(size):
				if FileUtil.moveImages(images,self.prepare_dir,self.queue_dir):
					return True
		return False

	def run(self,time_interval):
		while 1:
			time.sleep(time_interval)
			preImageNames = RedisUtil.get(self.num,"prepare")
			print preImageNames
			if preImageNames is None or len(preImageNames)==0:
				continue
			size = self._getImagesTotalSize(preImageNames)
			self._transfer(size)
			if RedisUtil.checkSize(size):
				allImages=RedisUtil.popAll()
				print allImages
				MapFileProducer(allImages,settings).run()

if __name__ == '__main__':
	server = Server(settings.prepare_dir,settings.queue_dir)
	server.run(settings.TIME_INTERVAL)