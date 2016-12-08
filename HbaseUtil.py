import settings
import happybase
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s:%(funcName)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',   
)

pool = happybase.ConnectionPool(size=settings.hbase_pool_size, \
								host=settings.hbase_host, \
								timeout=settings.hbase_time_out, \
								table_prefix=settings.hbase_table_prefix,\
								protocol='compact')
# conn = happybase.Connection(settings.hbase_host,table_prefix=settings.hbase_table_prefix)

def create_table(table_name=settings.hbase_table_name):
	try:
		with pool.connection() as conn:
			conn.create_table(table_name,{settings.hbase_family_image: dict(max_versions=1)})
	except Exception, e:
		logging.exception(e)
		return False
	return True

def write_image_path(image_path,row_key):
	try:
		with open(image_path,'rb') as f:
			imageBuffer = f.read()
			with pool.connection() as conn:
				table = conn.table(settings.hbase_table_name)
				table.put(row_key,{settings.hbase_family_image_buffer_coloum : imageBuffer})
	except Exception, e:
		logging.exception(e)
		return False
	return True

def write_image_buffer(imageId,imageBuffer):
	try:	
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)	
			table.put(imageId,{settings.hbase_family_image_buffer_coloum : imageBuffer})
	except Exception, e:
		logging.exception(e)
		return False
	return True

def write_images_buffer(images_buffer_dict):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)	
			with table.batch(batch_size=20) as b:
				for (imageId,imageBuffer) in images_buffer_dict.items():
					b.put(imageId,{settings.hbase_family_image_buffer_coloum : imageBuffer})
	except Exception, e:
		logging.exception(e)
		return False
	return True

def read_image_buffer(image_id):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)
			row = table.row(image_id)
			imageBuffer = row[settings.hbase_family_image_buffer_coloum]
	except Exception, e:
		logging.exception(e)
		return None
	return imageBuffer

def delete_image(image_id):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)
			table.delete(image_id)
	except Exception, e:
		logging.exception(e)
		return False
	return True

if __name__ == '__main__':
	# print create_table()
	write_image_path('/home/sxiong/Pictures/Video_8582/frame29.jpg','Video_8582-frame29.jpg')
	# read_image_buffer('Video_8582-frame1005')