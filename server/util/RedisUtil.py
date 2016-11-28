import sys
sys.path.append("../configs")
sys.path.append("configs")

import settings
import redis

pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db, max_connections=10)
r = redis.StrictRedis(connection_pool=pool)
IMAGE_QUEUE_KEY = "image_queue"
IMAGE_PREPARE_QUEUE_KEY = "image_prepare_queue"
IMAGE_SIZE_KEY = "image_toyal_size_byte"
MAPFILE_ID_KEY = "mapfile_id"
IMAGE_ID_TO_MAPFILEID_HASHSET_KEY = "iamge_id_to_mapfile_id"

def hmsetImageToMapfile(kvDict):
	try:
		r.hmset(IMAGE_ID_TO_MAPFILEID_HASHSET_KEY,kvDict)
	except Exception, e:
		print e
		return False
	return True

def hgetMapFileId(image_id):
	try:
		mapFileId = r.hget(IMAGE_ID_TO_MAPFILEID_HASHSET_KEY,image_id)
	except Exception, e:
		print e
		mapFileId = None
	return mapFileId

def getMapFileId():
	try:
	 	id = r.get(MAPFILE_ID_KEY)
	 	if id is None:
	 		id = "0"
	except Exception, e:
	 	print e 
	 	id = None
	return id

def increaseMapFileId():
	try:
		id = getMapFileId()
		if id is None:
			return False
		else:
			id = int(id)
			id = id + 1
			id = str(id)
			r.set(MAPFILE_ID_KEY,id)
	except Exception, e:
		print e
		return False
	return True

def pushPre(v):
	try:
		if type(v) is list:
			r.lpush(IMAGE_PREPARE_QUEUE_KEY,*v)
		elif type(v) is str:
			r.lpush(IMAGE_PREPARE_QUEUE_KEY,v)
		else:
			raise TypeError("type error")
	except Exception, e:
		print e
		return False
	return True

def popPre():
	try:
		allImages = r.lrange(IMAGE_PREPARE_QUEUE_KEY,0,-1)
		r.delete(IMAGE_PREPARE_QUEUE_KEY)
	except Exception, e:
		allImages = None
	return allImages

def push(v):
	try:
		if type(v) is list:
			r.lpush(IMAGE_QUEUE_KEY,*v)
		elif type(v) is str:
			r.lpush(IMAGE_QUEUE_KEY,v)
		else:
			raise TypeError("type error")
	except Exception, e:
		print e
		return false
	return True

def popAll():
	try:
		allImages = r.lrange(IMAGE_QUEUE_KEY,0,-1)
		r.delete(IMAGE_QUEUE_KEY)
	except Exception, e:
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
		print e
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
		print e
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
		print e
		return False

if __name__ == '__main__':
	# print addSize(1)
	# print checkSize(1)
	# print getMapFileId()
	# print increaseMapFileId()
	data = {"10":"0","11":"0"}
	hmsetImageToMapfile(data)