import settings
import bottle
from bottle import static_file

from bottle import request, response
from bottle import post, get, put, delete

import HbaseUtil

import os
import urllib
import pickle

@get('/api/image/<imageId>')
def get_image(imageId):
	imageBuffer = HbaseUtil.read_image_buffer(imageId)
	response.set_header('Content-type', 'image/jpeg')
	return imageBuffer

@delete('/api/image/<imageId>')
def del_image(imageId):
	HbaseUtil.delete_image(imageId)

@post('/api/image/<imageId>')
def post_image(imageId):
	_upload_image(imageId)

@put('/api/image/<imageId>')
def update_image(imageId):
	_upload_image(imageId)

def _upload_image(imageId):
	imageData = bottle.request.body.read()
	if imageData is not None:
		HbaseUtil.write_image_buffer(imageId,imageData)

@post('/api/images/')
def upload_images():
	images_buffer_str = bottle.request.body.read()
	images_buffer_dict = pickle.loads(images_buffer_str)

	HbaseUtil.write_images_buffer(images_buffer_dict)

def _save_buffer_to_file(imageBuffer):
	with open('test.jpg','wb') as f:
		f.write(imageBuffer)

if __name__ == '__main__':
	bottle.run(host = settings.api_host, port = settings.api_port)
