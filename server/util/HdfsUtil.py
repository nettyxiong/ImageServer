import hadoopy
import logging

def write(localpath,hdfspath):
    try:
        hadoopy.put(localpath,hdfspath)
    except Exception, e:
        logging.exception(e)
        return False
    return True

def copyFromHDFS(sourceMapfilePath,localDistPath):
    try:
        hadoopy.get(sourceMapfilePath,localDistPath)
    except Exception, e:
        logging.exception(e)
        return False
    return True