from flask import Flask, Blueprint, url_for
from flask_restx import Api
from celery import Celery, Task, registry

import os

import app_utils
import app_database
from deoldify_api import api as deoldify_api

# Configure CUDA
import fastai
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
ENABLE_GPU = os.getenv('ENABLE_GPU')
if ENABLE_GPU:
    device.set(device=DeviceId.GPU0)
    print("Running with GPU enabled...")
else:
    device.set(device=DeviceId.CPU)
    print("Running with only CPU enabled...")

# Import folders
from deoldify.visualize import *
os.environ['TORCH_HOME'] = '.'
torch.backends.cudnn.benchmark=True

app = Flask(__name__)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

api = Api(
    title='DeOldify API',
    version='1.0',
    doc=False
    # doc='/apidoc/'             # Set URL path for swagger
    # description='A description',
    # All API metadatas
)

api.namespaces.clear()
api.add_namespace(deoldify_api)
api.init_app(app)

# Configure Celery
# Configure through environment variables
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://172.17.0.2:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://172.17.0.2:6379/0')

app.config['task_routes'] = {'tasks_archive.*': {'queue': 'archive'}}
app.config['broker_url'] = CELERY_BROKER_URL
app.config['result_backend'] = CELERY_RESULT_BACKEND

celery = Celery(
            app.name, 
            broker=app.config['broker_url'], 
            backend=app.config['result_backend'],
            task_routes = app.config['task_routes'],
        )
celery.conf.update(app.config)
celery.conf.update(
    task_serializer='pickle',
    event_serializer='pickle',
    accept_content=['pickle','json'],
    worker_pool = 'solo',
)
# celery.conf.update(accept_content='pickle')

@app.route('/')
def hello():
    return {'placeholder': 'Welcome to the Colourize homepage'}

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')