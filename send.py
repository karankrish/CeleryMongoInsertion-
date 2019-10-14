import pika
import mysql.connector

def SendUrl(data):
    parameters = pika.URLParameters('amqp://user:bitnami@0.0.0.0:5672/')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='report-generator-queue')
    channel.basic_publish(exchange='', routing_key='report-generator-queue' ,body=str(data))
    connection.close()
    return 

def mysqlread():
    mydb = mysql.connector.connect(
      host="35.184.228.174",
      user="root",
      passwd="admin",
      database="wcag"
    )
    
    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT parseUrl FROM parseurltable;")
    
    myresult = mycursor.fetchall()
    a = []
    for i in myresult:
        a.append(i[0])
    return a
