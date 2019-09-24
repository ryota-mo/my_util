import json
import requests


def slack_notification(webhook_url, text, username=None, **kwargs):
    data = {'text': text, 'link_names': 1}
    if username:
        data.update({'username': username})
    if kwargs:
        data.update(kwargs)

    requests.post(webhook_url, data = json.dumps(data))
