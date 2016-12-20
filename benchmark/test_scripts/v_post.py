#coding=utf-8
import os
import mechanize
import time
import requests
import pickle
import sys
import random

POST_IMAGES_URL = "http://127.0.0.1:8000/api/images/"
POST_IMAGE_URL = "http://127.0.0.1:8000/api/image/"
def post_data(data,api_url=POST_IMAGES_URL):
	while True:
		r = requests.post(url=api_url,data=data,headers={'Connection':'close'})
		if r.status_code == 200:
			break
	return r.status_code

def _generete_image_id(videoName,imageName):
	return videoName + "-" + imageName

def generate_image_id(path):
	if not os.path.isdir(path) and  "." in path:
		temp = os.path.split(path)
		imageName = temp[1]
		videoName = os.path.split(temp[0])[1]
		return _generete_image_id(videoName,imageName)
	elif os.path.isdir(path):
		temp = os.path.split(path)
		if temp[1] == "":
			temp = os.path.split(temp[0])
		videoName = temp[1]

		return [_generete_image_id(videoName,imageName)  for imageName in os.listdir(path)]
	else:
		return None

def upload_images(path):
	if os.path.isdir(path) and "Video_" in path:
		imageIds = generate_image_id(path)
		image_buffer_dict = {}
		for imageId in imageIds:
			imageName = imageId.split("-")[-1]
			imagePath = os.path.join(path,imageName)
			with open(imagePath,'rb') as f:
				image_buffer_dict[imageId] = f.read()
		image_buffer_str = pickle.dumps(image_buffer_dict)
		post_data(image_buffer_str)
	elif os.path.isfile(path) and "Video_" in path:
		imageId = generate_image_id(path)
		with open(path,'rb') as f:
			image_buffer = f.read()
		post_data(image_buffer,POST_IMAGE_URL+imageId)
	else:
		print 'param path is not normal,please check it carefully'

from random import Random
def random_str(randomlength=20):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

class Transaction(object):
	def __init__(self):
		pass

	def run(self):
		
		image_path = '/home/sxiong/Pictures/Video_8582/frame29.jpg'
		# imageId = generate_image_id(image_path)
		imageId = random_str()

		start_time = time.time()
		with open(image_path,'rb') as f:
			image_buffer = f.read()
		# code = post_data(image_buffer,POST_IMAGE_URL+imageId)
		r = requests.post(url=POST_IMAGE_URL+imageId,data=image_buffer,headers={'Connection':'close'})
		code = r.status_code
		assert (code == 200), 'Bad Response: HTTP %s' % code
		# upload_images('/home/sxiong/Pictures/Video_8582/')
		self.custom_timers['POST'] = time.time() - start_time
