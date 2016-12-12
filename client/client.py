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
		dirpath = os.path.dirname(path)
		dirname = os.path.split(dirpath)[1]
		if "Video_" not in dirname:
			print 'miss video id in the path'
			return False
		else:
			basename = dirname + "-" + basename
		if checkIfImage(basename) and ScpUtil.putFile(path,os.path.join(settings.remote_dir,basename)):
			if RedisUtil.pushPre(basename):
				return True
	elif os.path.isdir(path):
		basenames = os.listdir(path)
		images = filterImages(basenames)
		dirname = os.path.split(path)[1]
		if dirname == "":
			dirname = os.path.split(os.path.split(path)[0])[1]
		print dirname
		if "Video_" not in dirname:
			print 'miss video id in the path'
			return False
		images = [dirname + "-" + imageid for imageid in images]
		print images
		if ScpUtil.putFiles(path,settings.remote_dir,dirname):
			if RedisUtil.pushPre(images):
				return True
	else:
		print 'image path is not right,neither a file or dir path'
	return False

'''
upload images in upper folder like "images/" but not "images/Video_8582"
'''
def putImagesUpperFolder(folder_path):
	folders = os.listdir(folder)
	folders = [f for f in folders if os.path.isdir(os.path.join(folder,f))]
	for folder_path in folders:
		putImagesToServer(folder_path)

'''
Usage:
python client.py '~/Pictures/Video_8582/frame29.jpg'
or
python client.py '~/Pictures/Video_8582/'
'''
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'missing argument please input the image path'
		exit(1)
	putImagesToServer(sys.argv[1])
	# putImagesToServer("/home/sxiong/Pictures/Video_8582/")