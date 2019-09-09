import datetime
import httplib2
import json
import os
import re
import sys

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run_flow as run
from pprint import pprint

class Struct:
    # simple non-recursive dict2obj class
    def __init__(self, **entries):
        self.__dict__.update(entries)

settings = json.load(open('settings.json'))
cfg = Struct(**settings)
today = datetime.datetime.now().strftime('%Y-%m-%d')

def get_auth(service):
    flow = flow_from_clientsecrets(cfg.oauth['client'],
        message=cfg.oauth['message'], scope=cfg.oauth['scope'])
    storage = Storage(cfg.oauth['storage'])
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run(flow, storage)
    return build(service, cfg.service[service],
        http=credentials.authorize(httplib2.Http()))

def reduce_results(obj, exclude=cfg.excludes, subdetails=False):
    item = { 'id': obj['id'] }

    snippet = obj['snippet']
    if exclude:
        item.update({k:snippet[k] for k in snippet.keys() if k not in exclude})
    else:
        item.update(snippet)

    details = obj['contentDetails']
    if subdetails:
        item.update(details[subdetails])
    else:
        item.update(details)

    return item

def get_channels(youtube):
    channels = []
    ch_request = youtube.channels().list(mine=True, part='snippet,contentDetails')
    #print(ch_request.to_json())
    ch_response = ch_request.execute()
    for channel in ch_response['items']:
        channels.append(reduce_results(channel, subdetails='relatedPlaylists'))
    return channels

def get_playlists(youtube):
    playlists = []
    pl_request = youtube.playlists().list(mine=True, part='snippet,contentDetails')
    #print(pl_request.to_json())
    while pl_request:
        pl_response = pl_request.execute()
        for playlist in pl_response['items']:
            playlists.append(reduce_results(playlist))
        pl_request = youtube.playlists().list_next(pl_request, pl_response)
    playlists.sort(key=lambda x: x['title'], reverse=True)
    return playlists

def list_uploads(youtube, playlist_id):
    uploads = []
    pl_request = youtube.playlistItems().list(playlistId=playlist_id, part='snippet,contentDetails')
    #print(pl_request.to_json())
    print('=====  Videos in list %s  =====' % playlist_id)
    while pl_request:
        pl_response = pl_request.execute()
        for pl_item in pl_response['items']:
            title = pl_item['snippet']['title']
            video_id = pl_item['snippet']['resourceId']['videoId']
            print('%s  %s' % (video_id, title))
            pprint(pl_item)
        pl_request = youtube.playlistItems().list_next(pl_request, pl_response)
    return uploads

def get_dimension(type):
    if type.startswith('d'):
        return 'day'
    elif type.startswith('m'):
        return 'month'
    elif type.startswith('v'):
        return 'video'
    else:
        return None

def get_end(type):
    if type.startswith('m'):
        return today[:8] + '01'
    return today

def get_start(type, channel):
    if type.startswith('m'):
        return channel['publishedAt'][:8] + '01'
    return channel['publishedAt'][:10]

def get_results(type):
    if type.startswith('v'):
        return '100'
    return None

def get_sort(type):
    if type.startswith('v'):
        return '-estimatedMinutesWatched'
    return None

def get_metrics(youtube, type, channel):
    metrics = []
    m_request = youtube.reports().query(
        ids='channel=='+channel['id'],
        endDate=get_end(type),
        startDate=get_start(type, channel),
        dimensions=get_dimension(type),
        maxResults=get_results(type),
        metrics=','.join(cfg.metrics),
        sort=get_sort(type)
    )
    #print(m_request.to_json())
    m_response = m_request.execute()
    pprint(m_response)
    pprint(m_response['columnHeaders'])

def usage():
    print('''Usage: %s <action>

    Actions:
        channels
        playlists
        videos [playlist_id]
        metrics [basic|daily|monthly|video]
        ''' % os.path.basename(sys.argv[0]))
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    action = sys.argv[1]
    youtube = get_auth('youtube')

    channels = get_channels(youtube)
    if action == 'channels':
        pprint(channels)
    elif action == 'playlists':
        pprint(get_playlists(youtube))
    elif action == 'videos':
        for ch in channels:
            playlist_id = ch['uploads']
        if len(sys.argv) > 2:
            playlist_id = sys.argv[2]
        if playlist_id:
            list_uploads(youtube, playlist_id)
        else:
            print('There is no uploaded videos playlist for this user.')
    elif action == 'metrics':
        youtube = get_auth('youtubeAnalytics')
        metric_type = 'basic'
        if len(sys.argv) > 2:
            metric_type = sys.argv[2]
        get_metrics(youtube, metric_type, channels[0])
    else:
        usage()
