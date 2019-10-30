#import pika
import mysql.connector
from datetime import datetime
from confluent_kafka import Producer

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.value()))



def SendUrl(data):
    """
    ###############RabbitMQ#################33
    parameters = pika.URLParameters('amqp://user:bitnami@0.0.0.0:5672/')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='report-generator-queue')
    channel.basic_publish(exchange='', routing_key='report-generator-queue' ,body=str(data))
    connection.close()
    """
    p = Producer({'bootstrap.servers': '35.239.53.243:9092'})

    try:
        domain = data["url"].split("//")[-1].split("/")[0].split('?')[0].replace("www.","")
        sendata = {'subscriptionDetailsId': 1,
 'domainId': int('%d'*len(domain) % tuple(map(ord, domain))),
 'active': True,
 'companyDomain': domain,
 'companyUrl': data["url"],
 'runStartDate': str(datetime.now()),
 'featureConfig': {'configId': 2,
  'linkAudit': True,
  'linkAuditCOnfiguration': {'linkAuditId': 2,
   'urlLimit': 10000,
   'crawlDepth': 5,
   'crawlDelay': 1,
   'remainingUrlCount': 10000},
  'pagespeedConfiguration': None},
 'userId': 2,
 'userStatus': 'subscribed_user',
 'user': None,
 'subscriptionPlan': None,
 'warned': False}
        p.produce('crawler-a11y',str(sendata).replace("False","false").replace("True","true").replace("None","null"), callback=acked)
        p.poll(0.5)
    except KeyboardInterrupt:
        pass
    
    p.flush(30)
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

def mysqlinsert(parseUrl):
    mydb = mysql.connector.connect(
      host="35.184.228.174",
      user="root",
      passwd="admin",
      database="wcag"
    )
    
    mycursor = mydb.cursor()
    
    sql = "INSERT INTO parseurltable (parseUrl, parseurlstatus) VALUES (%s, %s)"
    val = (parseUrl, "running")
    mycursor.execute(sql, val)
    
    mydb.commit()
    return 
