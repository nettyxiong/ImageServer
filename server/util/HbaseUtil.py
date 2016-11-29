import sys
sys.path.append("../configs")
sys.path.append("configs")
import settings

import happybase

conn = happybase.Connection(settings.hbase_host,table_prefix=settings.hbase_table_prefix)

def create_table(table_name):
	return conn.create_table(
		table_name,
		{'index': dict(max_versions=10),'data': dict(max_versions=10)}
	)

def put_index(tupleData):
	try:
		table = conn.table(settings.hbase_table_name)
		mapfileid = tupleData[0]
		keyDictData = tupleData[1]
		for (key,value) in keyDictData.items():
			data = {'index:mapfileid':mapfileid}
			table.put(key+'-'+value,data)
	except Exception, e:
		print e
		return False
	return True

def put_data(tupleData):
	try:
		table = conn.table(settings.hbase_table_name)
		mapfileid = tupleData[0]
		valueDataDict = tupleData[1]
		data = {}
		for (key,value) in valueDataDict.items():
			data['data:'+key] = value
		data['data:flag'] = '1'
		table.put(mapfileid,data)
	except Exception, e:
		print e
		return False
	return True

def put(tupleData):
	put_index(tupleData)
	put_data(tupleData)

def getByIndex(keyid,keyidName):
	try:
		table = conn.table(settings.hbase_table_name)
		row = table.row(keyidName+'-'+keyid)
		return row['index:mapfileid']
	except Exception, e:
		print e
		return None

def getByMapfileId(mapfileid):
	try:
		table = conn.table(settings.hbase_table_name)
		row = table.row(mapfileid)
		return row
	except Exception, e:
		print e
		return None

def _getVariableName(abc):
	abc_name = [ k for k,v in locals().iteritems() if v is abc][0]
	return abc_name

def test(imageid2):
	return _getVariableName(imageid2)
def init():
	create_table(settings.hbase_table_name)
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
	init()