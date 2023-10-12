import base64
import boto3
import json
import urllib3
from botocore.exceptions import ClientError
from pprint import pprint
from urllib.parse import parse_qs

APPLE_TEXT = 'Your+Apple+ID+Code+is'
ACCOUNT_SID = 'ABC123456789'
TEXT_NUMBER = '+11234567890'
SLACK_URL= 'https://your-company.slack.com/services/hooks/incoming-webhook'
SLACK_CHANNEL = 'channel'
SECRET_ID = 'secrets/manager/namespace/slack-webhook-' + SLACK_CHANNEL
REGION = 'us-east-1'

def msg(event, context):
    raw = base64.b64decode(event['body']).decode('ascii')
    qs = dict((k, v[-1] if isinstance(v, list) else v)
      for k, v in parse_qs(raw).items())
    # pprint(qs)
    
    if ACCOUNT_SID != qs.get('AccountSid'):
        return {
            'statusCode': 400,
            'body': 'Invalid Account'
        }
    if TEXT_NUMBER != qs.get('To'):
        return {
            'statusCode': 400,
            'body': 'Invalid SMS Number'
        }
    if not(qs.get('Body').startswith(APPLE_TEXT)):
        # print('Invalid Apple SMS')
        return {
            'statusCode': 400,
            'body': 'Invalid Apple SMS'
        }
        
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=REGION)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_ID)
    except ClientError as e:
        return {
            'statusCode': 400,
            'body': 'boto ' + e.response['Error']['Code']
        }

    slack_token = get_secret_value_response['SecretString']
    #print('%s?token=%s' % (SLACK_URL, slack_token))

    http = urllib3.PoolManager()
    response = http.request("POST",'%s?token=%s' % (SLACK_URL, slack_token),
        fields={
            'payload': json.dumps({
                'icon_emoji': ':applemac:',
                'text':       qs.get('Body'),
                'username':   'Apple ID',
            })
        })
    assert response.data.decode("utf-8") == 'ok'

    return {
        'statusCode': 200,
        'body': 'Posted SMS: %s' % qs.get('Body')
    }
