from flask import Flask, request
from flask_celery import make_celery
from pymongo import MongoClient
import json
from flask_cors import CORS
from send import SendUrl , mysqlread , mysqlinsert
from bson.objectid import ObjectId

with open('config.json') as f:
    config = json.load(f)
  
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://user:bitnami@0.0.0.0:5672'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
CORS(app)
celery = make_celery(app)


@app.route('/send', methods=['POST'])
def urlsend():
    try:
        data = request.json
        send.delay(data)
    except Exception as e:
        print("------rabbitmq api---------" +str(e))
    return "successfully send"

@celery.task(name="pgm.send")
def send(data):
    try:
        url = set(mysqlread())
        if data['url'] in url:
            pass
        else:
            SendUrl(data)
            mysqlinsert(data['url'])
    except Exception as e:
        print("------send task---------" +str(e))
    return "completed"

@app.route('/', methods=['POST'])
def process():
    try:
        data = request.json
        function.delay(data)
    except Exception as e:
        print("------flask api---------" +str(e))
    return "ok"

@app.route('/get', methods=['POST'])
def replace():
    try:
        data = request.json
        data = getData(data)
        for i in data:
           i['_id'] = str(i['_id']) 
    except Exception as e:
        print("------flask api---------" +str(e))
        data = [{}]
        
    return str(json.dumps(data))


def getData(d):
    try:
        client =MongoClient(config['mongodb']['host'],username=config['mongodb']['username'],password=config['mongodb']['password'],authSource=config['mongodb']['authSource'])
        db = client.DomainMonitor
        collection = db.api
        data = list(collection.find(d,{'_class':0}))
        client.close()
    except Exception as e:
        print("------getData---------" +str(e))
    return data

@app.route('/update', methods=['POST'])
def mongoupdation():
    try:
        data = request.json
        updated.delay(data)
    except Exception as e:
        print("------flask api---------" +str(e))
    return "ok"

@celery.task(name="pgm.updated")
def updated(data):
    try:
        client =MongoClient(config['mongodb']['host'],username=config['mongodb']['username'],password=config['mongodb']['password'],authSource=config['mongodb']['authSource'])
        db = client.DomainMonitor
        collection = db.api
        ID = data.pop('_id')
        collection.update({'_id': ObjectId(ID)},{'$set':data}, upsert=True, multi=False)
        client.close()
    except Exception as e:
        print("------DB---------" +str(e))
    return "completed"

@celery.task(name="pgm.function")
def function(data):
    try:
        client =MongoClient(config['mongodb']['host'],username=config['mongodb']['username'],password=config['mongodb']['password'],authSource=config['mongodb']['authSource'])
        db = client.DomainMonitor
        collection = db.api
        collection.insert_one(data)
        client.close()
    except Exception as e:
        print("------DB---------" +str(e))
    return "completed"

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
