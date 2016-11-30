#Hbase config
hbase_host="172.17.0.5"
hbase_table_prefix="imageserverv2"
hbase_table_name="image"
hbase_family_image="image_cf"
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
api_host="127.0.0.1"
api_port=8000



