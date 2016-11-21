#coding=utf-8
from util import RedisUtil
from util import ScpUtil
import settings
import os
import sys

def checkIfImage(basename):
	temp = basename.split(".")[-1]
	if temp not in ["jpg","jpeg","png"]:
		return False
	return True

def filterImages(basenames):
	images = [s for s in basenames if checkIfImage(s)]
	return images

def putImagesToServer(path):
	if os.path.isfile(path):
		basename = os.path.basename(path)
		if checkIfImage(basename) and ScpUtil.putFile(path,os.path.join(settings.remote_dir,basename)):
			if RedisUtil.pushPre(basename):
				return True
	elif os.path.isdir(path):
		basenames = os.listdir(path)
		images = filterImages(basenames)
		if ScpUtil.putFiles(path,settings.remote_dir):
			if RedisUtil.pushPre(images):
				return True
	else:
		print 'image path is not right,neither a file or dir path'
	return False

'''
Usage:
python client.py '~/Pictures/frame10.jpg'
or
python client.py '~/Pictures'
'''
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'missing argument please input the image path'
		exit(1)
	putImagesToServer(sys.argv[1])
	# putImagesToServer('/home/sxiong/Pictures/frame10.jpg')