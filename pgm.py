from flask import Flask, request
from flask_celery import make_celery
from pymongo import MongoClient
import json

with open('config.json') as f:
    config = json.load(f)
  
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://user:bitnami@localhost:5672'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = make_celery(app)

@app.route('/', methods=['PUT'])
def process():
	function.deplay(request.json)
	return "ok"

@celery.task(name="eg.function")
def function(j):
    data= {
            'url':request.json['url'],
            'error':request.json['error'],
            'remedy':request.json['remedy'],
            'remark':request.json['remark']
            }
    client =MongoClient(config['mongodb']['host'],
                                       username=config['mongodb']['username'],
                                       password=config['mongodb']['password'],
                                       authSource=config['mongodb']['authSource'])
    db = client.DomainMonitor
    collection = db.api
    collection.insert(data)
    return "completed"

if __name__ == "__main__":
    app.run(debug=True, host='localhost')