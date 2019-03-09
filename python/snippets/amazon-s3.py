import boto3
from io import StringIO

BUCKET = 'canvas-warehouse'

s3c = boto3.client('s3')
s3key = 'testing/storage'
contents = 'Something Blue'
s3c.put_object(Bucket = BUCKET, Key = s3key, Body = str(contents).encode('utf-8'), ACL = 'public-read')
print({ 'Success': '%s/%s' % (BUCKET, s3key) })

s3res = boto3.resource(service_name = 's3')
tmpfile = '/tmp/empty'
w = open(tmpfile, 'w')
w.write('Empty testing string')
w.close()
s3key = 'testing/empty'
s3res.meta.client.upload_file(Filename = tmpfile, Bucket = BUCKET, Key = s3key, ExtraArgs = {'ACL': 'public-read'})
#s3obj = s3res.Bucket(BUCKET).Object(s3key)
#s3obj.Acl().put(ACL='public-read')
print({ 'Success': '%s/%s' % (BUCKET, s3key) })
