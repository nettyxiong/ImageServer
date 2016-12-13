#coding=utf-8
from util import RedisUtil
from util import FileUtil

class ImageQueue:
	def __init__(self,prepare_dir,queue_dir):
		self.prepare_dir = prepare_dir
		self.queue_dir = queue_dir

	def transfer(self,num=100,size):
		images = RedisUtil.pop(num,"prepare")
		if images:
			if RedisUtil.push(images,"image") and RedisUtil.addSize(size):
				if FileUtil.moveImages(images,self.prepare_dir,self.queue_dir):
					return True
		return False

