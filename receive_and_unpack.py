#!/usr/bin/env python
import pika, sys, os, send, s3operations, io, json, zipfile, uuid

def main():
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='unpacker-queue')

    def callback(ch, method, properties, body):
        body_json = json.loads(body)
        bucket = body_json["Records"][0]["s3"]["bucket"]["name"]
        key = body_json["Records"][0]["s3"]["object"]["key"]

        content = s3operations.read_object_from_bucket(key, bucket)

        (unpacked_content, unpacked_filename) = unpack(content)
        print(' [*] Unpacked content ', unpacked_content)

        key = upload_unpacked_content(unpacked_content)
        print(' [*] Uploaded to bucket')

        notification_message = create_notification(body, unpacked_filename, key)
        send.send(pika.BasicProperties(), notification_message)

        print(' [*] Sent notification')
    
    channel.basic_consume(queue='unpacker-queue',
                      auto_ack=True,
                      on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def unpack(content):
    # Unzip the File
    zip = zipfile.ZipFile(BytesIO(content))
    zip_info = zip.infolist()
    # Just get the first file in the zip
    with zip.open(zip_info[0], 'r') as unzipped_file:
        return (unzipped_file.read(), zip_info[0].filename)

def upload_unpacked_content(unpacked_content):
    # Upload to S3
    key = uuid.uuid4()
    s3operations.upload_to_bucket(key, 'unpacked', io.BytesIO(bytearray(unpacked_content, 'utf-8')))
    return key

def create_notification(body, unpacked_filename, key):
    # Add to notification for formatter
    new_notifiction = {"unpacker": {"unpacked_filename": unpacked_filename, "bucket": "unpacked", "key": key}}
    body["Records"].append(new_notifiction)
    return json.dumps(body, indent=2)





if __name__ == '__main__':
    try:
        main()
    
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
