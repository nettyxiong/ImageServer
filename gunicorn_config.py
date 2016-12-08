import multiprocessing

bind = "0.0.0.0:8000"
workers = 4
# threads = 2*multiprocessing.cpu_count()+1
# work_connections = 1000
worker_class = "gevent"
reload = True
loglevel="info"