#!/usr/bin/env python
import pika, sys, os, send, s3operations, io

def main():
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='unpacker-queue')

    def callback(ch, method, properties, body):
        content = s3operations.read_object_from_bucket('input', 'Birthday2021.txt')
        print(' [*] Read from bucket ', content.len)
        unpacked_content = unpack(content)
        print(' [*] Unpacked content ', unpacked_content.len)
        upload_unpacked_content(unpacked_content)
        print(' [*] Uploaded to bucket')
        notification_message = create_notification(properties)
        send.send(pika.BasicProperties(), notification_message)
        print(' [*] Sent notification')
    
    channel.basic_consume(queue='unpacker-queue',
                      auto_ack=True,
                      on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def unpack(body):
    # Unzip the File
    return "This is the unpacked content"

def upload_unpacked_content(unpacked_content):
    # Upload to S3
    s3operations.upload_to_bucket('NewObject', 'unpacked', io.StringIO(unpacked_content))

def create_notification(properties):
    # Create notification for formatter
    return ("This is the notification for the formatter")





if __name__ == '__main__':
    try:
        main()
    
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
