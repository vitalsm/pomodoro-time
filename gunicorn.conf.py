import os

from dotenv import load_dotenv


bind = '0.0.0.0:8000'
workers = 4
worker_class = 'uvicorn_worker.UvicornWorker'
loglevel = 'info'
accesslog = '-'
errorlog = '-'

environment = os.getenv('ENVIRONMENT')
print(environment)
env = os.path.join(os.getcwd(), f'{environment}.env')
if os.path.exists(env):
    print(env)
    load_dotenv(env)
