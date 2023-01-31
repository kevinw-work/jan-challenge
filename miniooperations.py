from minio import Minio, credentials

def minio_client():
    # client = Minio(
    # endpoint='minio-kevin-w.flows-dev-cluster-7c309b11fc78649918d0c8b91bcb5925-0000.eu-gb.containers.appdomain.cloud',
    # access_key='b6J4Q7OXiGQZrCvp',
    # secret_key='CfQDpLK0xaKqZAsp2j1SAjKyBVEoal0F')
    client = Minio('localhost')
    buckets = client.list_buckets()
    print('Buckets are ', buckets)
    return client

def upload_to_bucket(object_key, bucket_name, fileobj):
    return minio_client().upload_file(fileobj, bucket_name, object_key)


def read_object_from_bucket(object_key, bucket_name):
    client = minio_client()
    exists = client.bucket_exists('input')
    print(' [*] Bucket exists? ', exists)
    return client.get_object(bucket_name=bucket_name, object_name=object_key)
