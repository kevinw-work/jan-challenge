import boto3

from boto3.s3.transfer import TransferConfig


def s3_client():
    # s3 = boto3.client('s3',
    # endpoint_url='https://c100-e.eu-gb.containers.cloud.ibm.com:30128',
    # aws_access_key_id='rpmoUwytb603LZN8',
    # aws_secret_access_key='c2UBIB8kGOJQcbjRQCYnw8tnXsVODUz2',
    # aws_session_token=None,
    # config=boto3.session.Config(signature_version='s3v4'),
    # verify=False)
    s3 = boto3.client('s3')
    """ :type : pyboto3.s3 """
    return s3

def upload_to_bucket(object_key, bucket_name, fileobj):
    return s3_client().upload_fileobj(fileobj, bucket_name, object_key)


def read_object_from_bucket(object_key, bucket_name):
    return s3_client().get_object(Bucket=bucket_name, Key=object_key)
