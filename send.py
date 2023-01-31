#!/usr/bin/env python
import pika

def send(properties, body):
    # note that in the openshift cluster we can simply use the service name 
    # (rabbitmq) to connect to the broker
#    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.basic_publish(exchange='dw',
                        routing_key='formatter-queue',
                        body=body,
                        properties=properties)

    print(" [x] Sent message to formatter")

    connection.close()
