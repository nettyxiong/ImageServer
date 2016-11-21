#coding=utf-8
import sys
sys.path.append("../configs")
sys.path.append("configs")
import settings

import paramiko
import os

hostname = settings.server_host
username = settings.ssh2_username
password = settings.ssh2_passwd
port = settings.ssh2_port

def _transferFiles(local_dir,remote_dir,flag="get"):
	try:
		t=paramiko.Transport((hostname,port))
		t.connect(username=username,password=password)
		sftp = paramiko.SFTPClient.from_transport(t)
		files = sftp.listdir(remote_dir)
		for f in files:
			if f.split(".")[-1] not in ["jpg","png","jpeg"]:
				continue
			if flag=="get":
				sftp.get(os.path.join(remote_dir,f),os.path.join(local_dir,f))
			else:
				sftp.put(os.path.join(local_dir,f),os.path.join(remote_dir,f))
		t.close()
		return True
	except Exception, e:
		print e
		return False

def getFiles(remote_dir,local_dir):
	return _transferFiles(local_dir,remote_dir,"get")

def putFiles(local_dir,remote_dir):
	return _transferFiles(local_dir,remote_dir,"put")

def _transferFile(local_path,remote_path,flag="get"):
	try:
		t = paramiko.Transport((hostname,port))
		t.connect(username=username, password=password)
		sftp = paramiko.SFTPClient.from_transport(t)
		if flag=="get":
			sftp.get(remote_path,local_path)
		else:
			sftp.put(local_path,remote_path)
		t.close()
		return True
	except Exception, e:
		print e
		return False
	
def getFile(remote_path,local_path):
	return _transferFile(local_path,remote_path,"get")

def putFile(local_path,remote_path):
	return _transferFile(local_path,remote_path,"put")

def delFiles(images):
	return True
	
if __name__ == '__main__':
	local_dir = "/home/sxiong/workspace/image-queue-py/preImages"
	remote_dir = "/home/sxiong/Pictures"
	getFiles(remote_dir,local_dir)
	putFiles(local_dir,remote_dir)

	local_path = '/home/sxiong/workspace/image-queue-py/client.py'
	remote_path = '/home/sxiong/workspace/client.py'
	getFile(remote_path,local_path)
	putFile(local_path,remote_path)
