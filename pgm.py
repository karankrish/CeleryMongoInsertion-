from flask import Flask, request
from flask_celery import make_celery
from pymongo import MongoClient
import json
from flask_cors import CORS

with open('config.json') as f:
    config = json.load(f)
  
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://user:bitnami@localhost:5672'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
CORS(app)
celery = make_celery(app)

@app.route('/', methods=['POST'])
def process():
    data = request.json
    function.delay(data)
    return "ok"
@celery.task(name="pgm.function")
def function(data):
  '''
    client =MongoClient(config['mongodb']['host'],
                                       username=config['mongodb']['username'],
                                       password=config['mongodb']['password'],
                                       authSource=config['mongodb']['authSource'])
  '''
    client =MongoClient(config['mongodb']['host'])
    db = client.DomainMonitor
    collection = db.api
    collection.insert(data)
    return "completed"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')