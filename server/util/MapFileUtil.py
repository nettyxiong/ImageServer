# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
sys.path.append("../configs")
sys.path.append("configs")
import settings

import HdfsUtil
import FileUtil

from hadoop.io import MapFile
from hadoop.io import Text

from os import listdir
from os.path import isfile, join

import pickle
import logging

PATH_NOT_EXISTS_MESSAGE=" has exists in local file system"

def createMapFile(images,mapFilePath='temp'):
	try:
		writer = MapFile.Writer(mapFilePath, Text, Text)
		for path in images:
			with open(join(settings.queue_dir,path),'rb') as f:
				data = f.read()
				data = pickle.dumps(data)
				key = Text()
				name = path.split("/")[-1].split(".")[0]
				key.set(name)
				value = Text()
				value.set(data)
				writer.append(key,value)

		writer.close()
	except Exception, e:
		logging.exception(e)
		return False
	return True

def readMapFileFromHdfs(mapFileId):
	sourceMapfilePath = join(settings.images_hdfs_path,mapFileId)
	localDistPath = join(settings.mapfile_cache_folder,mapFileId)
	if HdfsUtil.copyFromHDFS(sourceMapfilePath,localDistPath):
		return readMapFile(mapFileId)
	else:
		return False

def readMapFile(mapFileId,imageCachePath=settings.images_cache_folder):
	sourceMapfilePath = join(settings.mapfile_cache_folder,mapFileId)
	if not FileUtil.exists(sourceMapfilePath):
		logging.error(sourceMapfilePath + PATH_NOT_EXISTS_MESSAGE)
		return False

	try:
		key = Text()
		value = Text()
		reader = MapFile.Reader(sourceMapfilePath)
		while reader.next(key, value):
			data = pickle.loads(value.toString())
			# dir_path = join(imageCachePath,mapFileId)
			dir_path = imageCachePath
			if not FileUtil.exists(dir_path):
				FileUtil.mkdir(dir_path)
			image_path = join(dir_path,key.toString() + '.jpg')
			with open(image_path,'wb+') as f:
				f.write(data)
	except Exception, e:
		logging.exception(e)
		return False
	return True

def _readImages(mypath):
	images = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	return images

if __name__ == '__main__':
	# print help(io.MapFile.Writer)
	# print help(io.BytesWritable)
	mypath = '../images'
	images = _readImages(mypath)
	# print images
	# createMapFile(images)
	# readMapFile('temp')
	# print writeToHDFS('temp')
	# generateMapFileToHDFS(images,'1')
	readMapFile('1')