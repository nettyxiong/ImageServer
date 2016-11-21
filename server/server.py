from configs import settings
from util import RedisUtil
from util import MapFileUtil
from util import ScpUtil
import os
import time

def getImagesTotalSize(imagePaths):
	return sum(os.path.getsize(os.path.join(settings.prepare_dir,path)) for path in imagePaths)

def getAbsolutePaths(images,folder_path=settings.prepare_dir):
	return [os.path.join(folder_path,path) for path in images]

def main():
	while 1:
		time.sleep(settings.TIME_INTERVAL)
		preImageNames = RedisUtil.popPre()
		print preImageNames
		if preImageNames is None or len(preImageNames)==0:
			continue
		size = getImagesTotalSize(preImageNames)
		if not RedisUtil.checkSize(size):
			RedisUtil.push(preImageNames)
			RedisUtil.addSize(size)
			if ScpUtil.getFiles(settings.prepare_dir,settings.queue_dir):
				ScpUtil.delFiles(getAbsolutePaths(preImageNames))
		else:
			RedisUtil.push(preImageNames)
			allImages=RedisUtil.popAll()
			MapFileUtil.generateMapFileToHDFS(getAbsolutePaths(allImages,settings.queue_dir),RedisUtil.getMapFileId())
			RedisUtil.increaseMapFileId()

if __name__ == '__main__':
	main()