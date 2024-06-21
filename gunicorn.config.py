from environ import FileAwareEnv
from dotenv import load_dotenv, find_dotenv
from multiprocessing import cpu_count

env = FileAwareEnv()
load_dotenv(find_dotenv())

bind = '0.0.0.0:80'
workers = min(cpu_count(), 4) # don't hog system resources
reload = env.bool('GUNICORN_RELOAD', default=False)

# accesslog = '-' # skip access log (can get from nginx)
errorlog = '-'
loglevel = 'info' if env.bool('DEBUG', default=False) else 'error'
capture_output = True



