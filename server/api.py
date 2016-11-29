from configs import settings
import bottle
from bottle import static_file

from bottle import request, response
from bottle import post, get, put, delete

from util import HbaseUtil
from util import MapFileUtil
from os.path import join

@get('/api/images/<imageId>')
def getImage(imageId):
	'''
	get the Image data by imageId
	'''
	mapfileId = HbaseUtil.getByIndex(imageId,'imageId')
	if mapfileId is None:
		folder_path = settings.queue_dir
	else:
		MapFileUtil.loadImages(mapfileId)
		folder_path = join(settings.images_cache_folder,mapfileId)
	return static_file(imageId,root=folder_path,mimetype='image/jpg')

def _get_image_test(image_buffer,response):
	image_buffer = BytesIO()
	pi_camera.capture(image_buffer, format='jpeg')

	image_buffer.seek(0)
	bytes = image_buffer.read()
	response.set_header('Content-type', 'image/jpeg')
	return bytes


if __name__ == '__main__':
	bottle.run(server='gunicorn', host = settings.api_host, port = settings.api_port)