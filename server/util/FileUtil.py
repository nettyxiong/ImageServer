import shutil
from os.path import join
import os

import logging

'''
move images from prepare_dir to queue_dir
'''
def moveImages(images,srcFolder,dstFolder):
	try:
		for name in images:
			srcFilePath = join(srcFolder,name)
			move(srcFilePath,dstFolder)
	except Exception, e:
		logging.exception(e)
		return False
	return True

def move(src,dst):
	try:
		shutil.move(src,dst)
	except Exception, e:
		if type(e) != shutil.Error:
			logging.exception(e)
		return False
	return True

def copy(srcFilePath,dstFilePath):
	try:
		shutil.copy(srcFilePath,dstFilePath)
	except Exception, e:
		logging.exception(e)
		return False
	return True

def removeFile(path):
	try:
		os.remove(path)
	except Exception, e:
		logging.exception(e)
		return False
	return True

def removeFolder(path):
	try:
		shutil.rmtree(path)
	except Exception, e:
		logging.exception(e)
		return False
	return True
	
def exists(path):
	try:
		flag = os.path.exists(path)
	except Exception, e:
		logging.exception(e)
		flag = False
	return flag


def getAbsolutePaths(names,folder_path):
	results = None
	try:
		results = [os.path.join(folder_path,name) for name in names]
	except Exception, e:
		logging.exception(e)
		return None
	return results

def mkdir(path):
	try:
		os.mkdir(path)
	except Exception, e:
		logging.exception(e)
		return False
	return True

def makedirs(folder):
	try:
		os.makedirs(folder)
	except Exception, e:
		logging.exception(e)
		return False
	return True	

if __name__ == '__main__':
	copy('/home/sxiong/Pictures/1.txt','/home/sxiong/Pictures/Video_8582/1.txt')
	move('/home/sxiong/Pictures/Video_8582/1.txt','/home/sxiong/')
