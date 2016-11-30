import settings
import happybase
import os
pool = happybase.ConnectionPool(size=10, host=settings.hbase_host, table_prefix=settings.hbase_table_prefix)
# conn = happybase.Connection(settings.hbase_host,table_prefix=settings.hbase_table_prefix)

def create_table(table_name=settings.hbase_table_name):
	try:
		with pool.connection() as conn:
			conn.create_table(table_name,{settings.hbase_family_image: dict(max_versions=3)})
	except Exception, e:
		print e
		return False
	return True

def write_image_path(image_path):
	try:
		with open(image_path,'rb') as f:
			imageBuffer = f.read()
			row_key = os.path.split(image_path)[1]
			with pool.connection() as conn:
				table = conn.table(settings.hbase_table_name)
				table.put(row_key,{settings.hbase_family_image_buffer_coloum : imageBuffer})
	except Exception, e:
		print e
		return False
	return True

def write_image_buffer(imageId,imageBuffer):
	try:	
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)	
			table.put(imageId,{settings.hbase_family_image_buffer_coloum : imageBuffer})
	except Exception, e:
		print e
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
		print e
		return False
	return True

def read_image_buffer(image_id):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)
			row = table.row(image_id)
			imageBuffer = row[settings.hbase_family_image_buffer_coloum]
	except Exception, e:
		print e
		return None
	return imageBuffer

def delete_image(image_id):
	try:
		with pool.connection() as conn:
			table = conn.table(settings.hbase_table_name)
			table.delete(image_id)
	except Exception, e:
		print e
		return False
	return True

if __name__ == '__main__':
	# print create_table()
	write_image_path('/home/sxiong/workspace/ImageServer/images/preImages/Video_8582-frame1005.jpg')
	# read_image_buffer('Video_8582-frame1005')