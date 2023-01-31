import boto3

from boto3.s3.transfer import TransferConfig


def s3_client():
    s3 = boto3.client('s3',
    endpoint_url='http://minio-service.kevin-w.svc.cluster.local:9000',
    aws_access_key_id='b6J4Q7OXiGQZrCvp',
    aws_secret_access_key='CfQDpLK0xaKqZAsp2j1SAjKyBVEoal0F',
    verify=False)
    """ :type : pyboto3.s3 """
    return s3

def upload_to_bucket(object_key, bucket_name, fileobj):
    return s3_client().upload_fileobj(fileobj, bucket_name, object_key)


def read_object_from_bucket(object_key, bucket_name):
    return s3_client().get_object(Bucket=bucket_name, Key=object_key)
