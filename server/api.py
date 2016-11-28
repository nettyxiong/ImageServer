import bottle

from bottle import request, response
from bottle import post, get, put, delete

from util import HbaseUtil

_names = set()                    # the set of names

@post('/names')
def creation_handler():
	'''Handles name creation'''
	pass

@get('/names')
def listing_handler():
	'''Handles name listing'''
	pass

@put('/names/<name>')
def update_handler(name):
	'''Handles name updates'''
	pass

@delete('/names/<name>')
def delete_handler(name):
	'''Handles name deletions'''
	pass

@get('/api/images/<imageId>')
def getImage(imageId):
	'''
	get the Image data by imageId
	'''
	mapfileId = HbaseUtil.getByIndex(imageId,'imageId')
	if mapfileId is None:
		pass
	else:
		pass



if __name__ == '__main__':
	bottle.run(server='gunicorn', host = '127.0.0.1', port = 8000)