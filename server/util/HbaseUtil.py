#coding=utf-8
import sys
sys.path.append("../configs")
sys.path.append("configs")
import settings

import happybase
import json
import logging
pool = happybase.ConnectionPool(size=settings.hbase_pool_size, \
								host=settings.hbase_host, \
								table_prefix=settings.hbase_table_prefix,\
								protocol='compact')

# conn = happybase.Connection(host=settings.hbase_host,\
# 							table_prefix=settings.hbase_table_prefix,\
# 							protocol="compact")

def create_table(table_name):
	try:
		with pool.connection() as conn:
			conn.create_table(table_name, {'index': dict(max_versions=1),'data': dict(max_versions=1)})
	except Exception, e:
		logging.exception(e)
		return False
	return True

#row key is imageId,data is mapfileId
def put_index(dictData):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)
			with table.batch(batch_size=20) as b:
				for (key,value) in dictData.items():
					data = {'index:mapfileid':value}
					imageId = key
					b.put(imageId,data)
	except Exception, e:
		logging.exception(e)
		return False
	return True

#row key is mapfileId,data is imageId
def put_data(dictData):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)
			imageIds = dictData.keys()
			mapfileId = dictData.values()[0]
			table.put(mapfileId,{'data:imageIds':json.dumps(imageIds)})
	except Exception, e:
		logging.exception(e)
		return False
	return True

def put(data):
	return put_index(data) and put_data(data)
	
def getImageIds(mapfileId):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)
			row = table.row(mapfileId)
			imageIds = json.loads(row['data:imageIds'])
	except Exception, e:
		logging.exception(e)
		imageIds = None
	return imageIds

def getMapFileId(imageId):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)
			row = table.row(imageId)
			logging.info(row)
			mapfileId = row['index:mapfileid']
	except Exception, e:
		logging.exception(e)
		mapfileId = None
	return mapfileId

def init():
	create_table(settings.hbase_table_name)

def _test():
	with pool.connection() as conn:
		table = conn.table('image')
		row = table.row('Video_8582-frame915.jpg')
		print row


if __name__ == '__main__':
	# init()
	# conn = happybase.Connection("172.19.0.2")
	# create_table('sxiong3')
	# table = conn.table('sxiong3')
	# print table
	# # table.put(b'row-key', {b'cf:col1': b'value1',b'cf:col2': b'value2'})
	# # table.put(b'row-key', {b'cf1:col1': b'value1'}, timestamp=123456789)
	# row = table.row(b'row-key')
	# print row[b'cf1:col1']
	# data = ('2',{'imageid':'1223','videoid':'1111','frameid':'111'})
	# print put_index(data)
	# print put_data(data)
	# imageid2 = '111'
	# print test(imageid2)
	# table = conn.table(settings.hbase_table_name)
	# print type(table.row('1'))
	# print table.row('1')
	_test()