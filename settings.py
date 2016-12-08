#Hbase config
hbase_host="172.17.0.5"
# hbase_host="202.114.18.78"
hbase_pool_size=10
#milliseconds
hbase_time_out=None
hbase_table_prefix="v2"
hbase_table_name="image"
hbase_family_image="cf"
hbase_family_image_buffer_coloum=hbase_family_image+":imageBuffer"

#image table 
'''
table_name:image
----row-key:imageId
----cf_name:image_cf
--------imageBuffer
--------videoId
'''
#api service config
api_host="0.0.0.0"
api_port=8000



