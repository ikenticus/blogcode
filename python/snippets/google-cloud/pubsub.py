
# pip install --upgrade google-cloud-pubsub psq
from google.cloud import pubsub

import json
import os
import psq
import sys
import time

def get_message(project_id, subscription_name):
    subscriber = pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback_subscribe(message):
        print('Received message: {}'.format(message))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback_subscribe)
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)

def put_message(project_id, topic_name):
    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    def callback_publish(message_future):
        # When timeout is unspecified, the exception method waits indefinitely.
        if message_future.exception(timeout=30):
            print('Publishing message on {} threw an Exception {}.'.format(
                topic_name, message_future.exception()))
        else:
            print(message_future.result())

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        # When you publish a message, the client returns a Future.
        message_future = publisher.publish(topic_path, data=data)
        message_future.add_done_callback(callback_publish)

    print('Published message IDs:')

    # We must keep the main thread from exiting to allow it to process
    # messages in the background.
    while True:
        time.sleep(60)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '''\nUsage: %s key.json <action> <queue> <params>

        get <subscription>
        put <topic>
        ''' % os.path.basename(sys.argv[0])
        sys.exit(1);

    key_file = sys.argv[1]
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file
    with open(key_file) as f:
        creds = json.load(f)
    project_id = creds['project_id']

    #publisher = pubsub.PublisherClient()
    #subscriber = pubsub.SubscriberClient()
    #q = psq.Queue(publisher, subscriber, project_id)

    action = sys.argv[2]
    name = sys.argv[3]
    switcher = {
        'get': get_message,
        'put': put_message
    }
    func = switcher.get(action, 'Invalid Action')
    func(project_id, name)
