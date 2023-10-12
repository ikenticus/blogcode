import boto3
import requests
from botocore.exceptions import ClientError
from chalice import Chalice, Response
from pprint import pprint
from urllib.parse import parse_qs

app = Chalice(app_name='twilio_slack_hook')
app.api.binary_types.append('application/x-www-form-urlencoded')

APPLE_TEXT = 'Your+Apple+ID+Code+is'
ACCOUNT_SID = 'ABC123456789'
TEXT_NUMBER = '+11234567890'
SLACK_URL= 'https://your-company.slack.com/services/hooks/incoming-webhook'
SLACK_CHANNEL = 'channel'
SECRET_ID = 'secrets/manager/namespace/slack-webhook-' + SLACK_CHANNEL
REGION = 'us-east-1'

@app.route('/', methods=['POST'], content_types=['application/x-www-form-urlencoded'])
def msg():
    raw = app.current_request.raw_body.decode('ascii')
    qs = dict((k, v[-1] if isinstance(v, list) else v)
      for k, v in parse_qs(raw).items())
    #pprint(qs)

    if ACCOUNT_SID != qs.get('AccountSid'):
        return Response(status_code=400, body={'message': 'Invalid Account'})
    if TEXT_NUMBER != qs.get('To'):
        return Response(status_code=400, body={'message': 'Invalid SMS Number'})
    if not(qs.get('Body').startswith(APPLE_TEXT)):
        # print('Invalid Apple SMS')
        return Response(status_code=400, body={'message': 'Invalid Apple SMS'})

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=REGION)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=SECRET_ID)
    except ClientError as e:
        return Response(status_code=400, body={'message': 'boto ' + e.response['Error']['Code']})

    slack_token = get_secret_value_response['SecretString']
    #print('%s?token=%s' % (SLACK_URL, slack_token))

    response = requests.post(url='%s?token=%s' % (SLACK_URL, slack_token), json={
            'icon_emoji': ':applemac:',
            'text':       qs.get('Body'),
            'username':   'Apple ID',
    }, verify=False)
    assert response.status_code == 200

    return Response(status_code=200, body={'message': 'Posted SMS: %s' % qs.get('Body')})
