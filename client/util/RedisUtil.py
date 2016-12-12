import sys
sys.path.append("..")
import settings

import redis
import logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',   
)

pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db, max_connections=10)
r = redis.StrictRedis(connection_pool=pool)
IMAGE_QUEUE_KEY = "image_queue"
IMAGE_PREPARE_QUEUE_KEY = "image_prepare_queue"
IMAGE_SIZE_KEY = "image_toyal_size_byte"


def pushPre(v):
	try:
		if type(v) is list: 
			r.lpush(IMAGE_PREPARE_QUEUE_KEY,*v)
		elif type(v) is str:
			r.lpush(IMAGE_PREPARE_QUEUE_KEY,v)
	except Exception, e:
		logging.exception(e)
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
		r.lpush(IMAGE_QUEUE_KEY,v)
	except Exception, e:
		logging.exception(e)
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
	pushPre(['test','111'])