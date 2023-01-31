#!/usr/bin/env python
import sys, os, s3operations, miniooperations

def main():
    minio_object_content = miniooperations.read_object_from_bucket(object_key='Birthday2021.txt', bucket_name='input')
    print('Read a minio object')
    s3_object_content = s3operations.read_object_from_bucket(object_key='Birthday2021.txt', bucket_name='input')
    print('Read an s3 object')
    
if __name__ == '__main__':
    try:
        main()
    
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
