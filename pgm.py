from flask import Flask, request
from flask_celery import make_celery
from pymongo import MongoClient
import json
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler


logging.basicConfig(filename='log/api.log', level=logging.ERROR, 
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger("api.log")
handler = RotatingFileHandler("log/api.log", maxBytes=2000, backupCount=25) 
if not logger: 
    logger.addHandler(handler)
    
    

with open('config.json') as f:
    config = json.load(f)
  
app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://user:bitnami@0.0.0.0:5672'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
CORS(app)
celery = make_celery(app)

@app.route('/', methods=['POST'])
def process():
    try:
        data = request.json
        function.delay(data)
    except Exception as e:
        logger.error("------flask api---------" +str(e))
    return "ok"
@celery.task(name="pgm.function")
def function(data):
    try:
        client =MongoClient(config['mongodb']['host'],username=config['mongodb']['username'],password=config['mongodb']['password'],authSource=config['mongodb']['authSource'])
        db = client.DomainMonitor
        collection = db.api
        collection.insert(data)
    except Exception as e:
        logger.error("------DB---------" +str(e))
    return "completed"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
