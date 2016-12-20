import os
import mechanize
import time
import requests

class Transaction(object):
	def __init__(self):
		self.custom_timers = {}
		# self.api_url = 'http://127.0.0.1:82/api/image/Video_8582-frame800.jpg'
		self.api_url = 'https://www.baidu.com'

	def run(self):

		# start_time = time.time()
		# r = requests.get(api_url,headers={'Connection':'close'})
		# code = r.status_code
		# assert (code == 200), 'Bad Response: HTTP %s' % code
		# self.custom_timers['GET'] = time.time() - start_time

		br = mechanize.Browser()
		br.set_handle_robots(False)
		start_time = time.time()
		resp = br.open(self.api_url)
		code =resp.code
		assert (code == 200), 'Bad Response: HTTP %s' % code
		self.custom_timers['GET'] = time.time() - start_time

		# br = mechanize.Browser()
		# br.set_handle_robots(False)
		# imageIds = os.listdir('/home/sxiong/Pictures/Video_8582/')
		# start_time = time.time()
		# for id in imageIds:
		# 	api_url = 'http://127.0.0.1:8000/api/image/'+ 'Video_8582-' + id
		# 	# print api_url
		# 	resp = br.open(api_url)
		# 	assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.codes
		# for id in imageIds:
		# 	api_url = 'http://127.0.0.1:8000/api/image/'+ 'Video_8582-' + id
		# 	# print api_url
		# 	resp = br.open(api_url)
		# 	assert (resp.code == 200), 'Bad Response: HTTP %s' % resp.codes
		# self.custom_timers['GET'] = time.time() - start_time
