import os

import boto3
s3c = boto3.client('s3')
s3res = boto3.resource(service_name = 's3')

BUCKET = 'canvas-warehouse'

def put_object(s3key, contents):
    s3c.put_object(Bucket=BUCKET, Key=s3key, Body=str(contents).encode('utf-8'), ACL='public-read')
    return { 'Success': '%s/%s' % (BUCKET, s3key) }

def upload_file(s3key, contents, tmpfile):
    w = open(tmpfile, 'w')
    w.write(contents)
    w.close()
    s3res.meta.client.upload_file(Filename=tmpfile, Bucket=BUCKET, Key=s3key, ExtraArgs={'ACL': 'public-read'})
    #s3obj = s3res.Bucket(BUCKET).Object(s3key)
    #s3obj.Acl().put(ACL='public-read')
    return { 'Success': '%s/%s' % (BUCKET, s3key) }

def move_objects(source, dest):
    #listing = s3res.meta.client.list_objects(Bucket=BUCKET, Prefix=source)
    listing = s3c.list_objects(Bucket=BUCKET, Prefix=source)
    for obj in listing.get('Contents'):
        s3key = obj.get('Key')
        target = s3key.replace(source, dest)
        print(target)
        copy_source = {'Bucket': BUCKET, 'Key': s3key}
        s3c.copy_object(CopySource=copy_source, Bucket=BUCKET, Key=target)
        s3c.delete_object(Bucket=BUCKET, Key=s3key)

if __name__ == '__main__':
    print(put_object('testing/storage', 'Something New'))
    #print(upload_file('testing/storage', 'Something Blue', '/tmp/empty'))
    move_objects('testing', 'moved')
