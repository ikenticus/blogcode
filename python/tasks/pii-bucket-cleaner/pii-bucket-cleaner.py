import boto3
import json
import re

class Struct:
    # simple non-recursive dict2obj class
    def __init__(self, **entries):
        self.__dict__.update(entries)

settings = json.load(open('settings.json'))
cfg = Struct(**settings)

s3 = boto3.client(
    's3',
    aws_access_key_id=cfg.access,
    aws_secret_access_key=cfg.secret,
)

dob_patt = re.compile(r"DOB='.*(\d+)/(\d+)/(\d+)[^']*'")

def get_objects():
    listing = s3.list_objects(Bucket=cfg.bucket)
    if not listing.get('Contents'):
        print('\nNo files found')
        return
    for obj in listing.get('Contents'):
        filename = obj.get('Key')
        if filename == 'patients.log':
            # print(clean_dob(filename))
            s3.put_object(Body=clean_dob(filename), Bucket=cfg.bucket, Key=filename)

def clean_dob(filename):
    clean = []
    data = s3.get_object(Bucket=cfg.bucket, Key=filename)['Body'].read().decode('utf-8')
    for d in data.split('\n'):
        if 'DOB' in d:
            clean.append(dob_patt.sub(r"DOB='X/X/\3'", d))
        else:
            clean.append(d)
    return '\n'.join(clean)

if __name__ == '__main__':
    get_objects()
