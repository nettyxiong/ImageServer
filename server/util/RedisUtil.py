import sys
sys.path.append("../configs")
sys.path.append("configs")

import settings
import redis
import logging

pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db, max_connections=10)
r = redis.StrictRedis(connection_pool=pool)
IMAGE_QUEUE_KEY = "image_queue"
IMAGE_PREPARE_QUEUE_KEY = "image_prepare_queue"
IMAGE_SIZE_KEY = "image_total_size_byte"
IMAGE_ID_TO_MAPFILEID_HASHSET_KEY = "iamge_id_to_mapfile_id"

def hmsetImageToMapfile(kvDict):
	try:
		r.hmset(IMAGE_ID_TO_MAPFILEID_HASHSET_KEY,kvDict)
	except Exception, e:
		logging.exception(e)
		return False
	return True

def _init_queue_name(kind):
	if kind=="prepare":
		queue_name = IMAGE_PREPARE_QUEUE_KEY
	elif kind == "image":
		queue_name = IMAGE_QUEUE_KEY
	else:
		logging.exception("kind error,either 'prepare' or 'image'")
		return None
	return queue_name

def _push(v,queue_name):
	try:
		if type(v) is list:
			r.lpush(queue_name,*v)
		elif type(v) is str:
			r.lpush(queue_name,v)
		else:
			raise TypeError("type error")
	except Exception, e:
		logging.exception(e)
		return False
	return True

def _pop(num,queue_name):
	try:
		images = r.lrange(queue_name,0,num)
		r.ltrim(queue_name,num+1,-1)
	except Exception, e:
		logging.exception(e)
		images = None
	return images

def _get(num,queue_name):
	try:
		images = r.lrange(queue_name,0,num)
	except Exception, e:
		logging.exception(e)
		images = None
	return images

def push(v,kind="image"):
	queue_name = _init_queue_name(kind)
	if queue_name:
		return _push(v,queue_name)
	else:
		return False

def pop(num,kind="image"):
	queue_name = _init_queue_name(kind)
	if queue_name:
		return _pop(num,queue_name)
	else:
		return None

def get(num,kind="image"):
	queue_name = _init_queue_name(kind)
	if queue_name:
		return _get(num,queue_name)
	else:
		return None	

def popAll(kind="image"):
	queue_name = _init_queue_name(kind)
	try:
		allImages = r.lrange(queue_name,0,-1)
		r.delete(IMAGE_QUEUE_KEY)
	except Exception, e:
		logging.exception(e)
		allImages = None
	return allImages

def addSize(size):
	try:
		total = r.get(IMAGE_SIZE_KEY)
		if total is None:
			total = 0
		else:
			total = int(total)
		total += size
		r.set(IMAGE_SIZE_KEY,total)
	except Exception, e:
		logging.exception(e)
		return False
	return True

def getSize():
	try:
		size = r.get(IMAGE_SIZE_KEY)
		if size is None:
			size = 0
		else:
			size = int(size)
	except Exception, e:
		logging.exception(e)
		size = 0
	return size

def checkSize(size):
	try:
		total = getSize()
		if total + size >= settings.MAX_IMAGE_SIZE:
			return True
		else:
			return False
	except Exception, e:
		logging.exception(e)
		return False

if __name__ == '__main__':
	# print addSize(1)
	# print checkSize(1)
	# print getMapFileId()
	# print increaseMapFileId()
	# data = {"10":"0","11":"0"}
	# hmsetImageToMapfile(data)
	print r.lrange(IMAGE_PREPARE_QUEUE_KEY,0,100)