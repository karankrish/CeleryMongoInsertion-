import pika
def SendUrl(data):
    parameters = pika.URLParameters('amqp://user:bitnami@localhost:5672/')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='url')
    channel.basic_publish(exchange='', routing_key='url', body=str(data))
    connection.close()
    return 
