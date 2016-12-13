#/usr/bin/env python
#coding=utf-8

from configs import settings
from util import FileUtil
import logging
logging.basicConfig(
	level=logging.INFO,
	format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
	datefmt='%Y-%m-%d %H:%M:%S',   
)

def init():
	folders = [settings.prepare_dir,settings.queue_dir,\
	settings.images_cache_folder,settings.mapfile_cache_folder]
	for path in folders:
		if not FileUtil.exists(path):
			if not FileUtil.makedirs(path):
				logging.error('init error...')
				break
	logging.info('init success...')

if __name__ == '__main__':
	init()
