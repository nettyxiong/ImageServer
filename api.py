import settings
import bottle
from bottle import static_file
from bottle import request, response
from bottle import post, get, put, delete

import HbaseUtil

import os
import pickle

@get('/api/image/<imageId>')
def get_image(imageId):
	imageBuffer = HbaseUtil.read_image_buffer(imageId)
	response.set_header('Content-type', 'image/jpeg')
	if imageBuffer is None:
		response.status = 404
	return imageBuffer

@delete('/api/image/<imageId>')
def del_image(imageId):
	if HbaseUtil.delete_image(imageId):
		response.status = 200
	else:
		response.status = 500

@post('/api/image/<imageId>')
def post_image(imageId):
	if _upload_image(imageId):
		response.status = 200
	else:
		response.status = 500

@put('/api/image/<imageId>')
def update_image(imageId):
	if _upload_image(imageId):
		response.status = 200
	else:
		response.status = 500

def _upload_image(imageId):
	imageData = bottle.request.body.read()
	if imageData is not None:
		return HbaseUtil.write_image_buffer(imageId,imageData)
	else:
		return False

@post('/api/images/')
def upload_images():
	images_buffer_str = bottle.request.body.read()
	images_buffer_dict = pickle.loads(images_buffer_str)

	if HbaseUtil.write_images_buffer(images_buffer_dict):
		response.status = 200
	else:
		response.status = 500

def _save_buffer_to_file(imageBuffer):
	with open('test.jpg','wb') as f:
		f.write(imageBuffer)

if __name__ == '__main__':
	# bottle.run(server='gunicorn', host = settings.api_host, port = settings.api_port,workers=4)
	bottle.run(host = settings.api_host, port = settings.api_port)

app = bottle.default_app()
