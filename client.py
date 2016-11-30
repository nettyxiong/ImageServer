#coding=utf-8
import requests
import os
import pickle
POST_IMAGES_URL = "http://127.0.0.1:8000/api/images/"
POST_IMAGE_URL = "http://127.0.0.1:8000/api/image/"
def post_data(data,api_url=POST_IMAGES_URL):
	while True:
		r = requests.post(url=api_url,data=data)
		if r.status_code == 200:
			break
	print r.status_code

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


'''
Usage:
python client.py '/home/sxiong/Pictures/Video_8582/frame29.jpg'
or
python client.py '/home/sxiong/Pictures/Video_8582/'
or
python client.py '/home/sxiong/Pictures/Video_8582'
'''
if __name__ == '__main__':
	# print generate_image_id('/home/sxiong/Pictures/Video_8582/frame29.jpg')
	# print generate_image_id('/home/sxiong/Pictures/Video_8582/')
	# print generate_image_id('/home/sxiong/Pictures/Video_8582')

	# upload_images('/home/sxiong/Pictures/Video_8582/frame29.jpg')
	# upload_images('/home/sxiong/Pictures/Video_8582/')
	# upload_images('/home/sxiong/Pictures/Video_8582')

	if len(sys.argv) < 2:
		print 'missing argument please input the image path'
		exit(1)
	upload_images(sys.argv[1])