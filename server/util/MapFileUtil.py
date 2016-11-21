# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
sys.path.append("../configs")
sys.path.append("configs")
import settings

from hadoop.io.IntWritable import LongWritable
from hadoop.io import MapFile
from hadoop.io import Text

import hadoopy

from os import listdir
from os.path import isfile, join
from os import rmdir
import pickle

import shutil

def _createMapFile(images,mapFilePath='temp'):
    writer = MapFile.Writer(mapFilePath, Text, Text)
    for path in images:
        print path
        with open(path,'rb') as f:
            data = f.read()
            data = pickle.dumps(data)
            key = Text()
            name = path.split("/")[-1].split(".")[0]
            key.set(name)
            value = Text()
            value.set(data)
            writer.append(key,value)

    writer.close()
    return mapFilePath

def readImages(folder):
    images = [ join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f)) ]
    return images

def readMapFile(sourceMapfilePath,localDistPath=''):
    key = Text()
    value = Text()
    reader = MapFile.Reader(sourceMapfilePath)
    while reader.next(key, value):
        data = pickle.loads(value.toString())
        with open(localPath+key.toString()+'.jpg','wb+') as f:
            f.write(data)

def _writeToHDFS(mapFilePath='temp'):
    try:
        hadoopy.put(mapFilePath,settings.images_hdfs_path)
    except Exception, e:
        print e
        return False
    return True

def _delMapFile(mapFilePath='temp'):
    shutil.rmtree(mapFilePath)

def generateMapFileToHDFS(images,mapFileId):
    _createMapFile(images,mapFileId)
    _writeToHDFS(mapFileId)
    _delMapFile(mapFileId)


if __name__ == '__main__':
    # print help(io.MapFile.Writer)
    # print help(io.BytesWritable)
    mypath = '../images'
    images = readImages(mypath)
    # createMapFile(images)
    # readMapFile('temp')
    # print writeToHDFS('temp')
    generateMapFileToHDFS(images)