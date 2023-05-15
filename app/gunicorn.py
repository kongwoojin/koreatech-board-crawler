# Socket Path
bind = 'unix:/home/kongjak/CSE_crawler_API/gunicorn.sock'

# Worker Options
workers = 2
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/kongjak/CSE_crawler_API/access_log'
errorlog = '/home/kongjak/CSE_crawler_API/error_log'
