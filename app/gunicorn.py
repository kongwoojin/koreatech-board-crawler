import os
import multiprocessing

# Socket Path
bind = '0.0.0.0:8000'

# Worker Options
workers = multiprocessing.cpu_count()
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = f'{os.getcwd()}/access_log'
errorlog = f'{os.getcwd()}/error_log'
