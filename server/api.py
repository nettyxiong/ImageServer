from configs import settings
import bottle
from bottle import static_file
from bottle import request, response
from bottle import post, get, put, delete

from util import FileUtil
from util import HbaseUtil
from util import MapFileUtil
from os.path import join

import logging
logging.basicConfig(
	level=logging.INFO,
	format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
	datefmt='%Y-%m-%d %H:%M:%S',   
)

@get('/api/image/<imageId>')
def getImage(imageId):
	if not FileUtil.exists(join(settings.images_cache_folder,imageId)):
		mapfileId = HbaseUtil.getMapFileId(imageId)
		logging.info(mapfileId)
		if mapfileId is None:
			logging.error('404')
			response.status = 404
			return
		if FileUtil.exists(join(settings.mapfile_cache_folder,mapfileId)):
			MapFileUtil.readMapFile(mapfileId)
		else:
			MapFileUtil.readMapFileFromHdfs(mapfileId)
	# folder_path = join(settings.images_cache_folder,mapfileId)
	folder_path = settings.images_cache_folder
	logging.info(folder_path)
	return static_file(imageId,root=folder_path,mimetype='image/jpg')

if __name__ == '__main__':
	bottle.run(host = settings.api_host, port = settings.api_port)
	# bottle.run(server='gunicorn', host = settings.api_host, port = settings.api_port)
else:
	app = application = bottle.default_app()
