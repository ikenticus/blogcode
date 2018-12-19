
# pip install --upgrade google-cloud-storage
from google.cloud import storage

import os
import sys

def create_bucket(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created'.format(bucket.name))

def list_blobs(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        print(blob.name)

def read_blob(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(sys.stdout)

def write_blob(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(sys.stdin)

def delete_blob(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print('Blob {} deleted.'.format(blob_name))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print '''\nUsage: %s key.json <action> <params>

        create <bucket>
        list <bucket>
        read <bucket> <blob>
        write <bucket> <blob>
        delete <bucket> <blob>
        ''' % os.path.basename(sys.argv[0])
        sys.exit(1);

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = sys.argv[1]
    action = sys.argv[2]
    bucket_name = sys.argv[3]
    switcher = {
        'create': create_bucket,
        'list': list_blobs,
        'read': read_blob,
        'write': write_blob,
        'delete': delete_blob
    }
    func = switcher.get(action, 'Invalid Action')
    blob_name = '' if len(sys.argv) < 4 else sys.argv[4]
    func(bucket_name, blob_name);
    # using python 2.7 the google-cloud credentials do NOT appear to be working
