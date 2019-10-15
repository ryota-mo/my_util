import os
import json


def is_file_or_raw_text(input):
    if os.path.isfile(input):
        # if input is file, read file
        with open(input, 'r') as f:
            output = f.read().rstrip('\n')
    else:
        output = input
    return output


def slack_notification(text, webhook_url, username=None, **kwargs):
    import requests
    webhook_url = is_file_or_raw_text(webhook_url)
    data = {'text': text, 'link_names': 1}
    if username:
        data.update({'username': username})
    if kwargs:
        data.update(kwargs)

    requests.post(webhook_url, data=json.dumps(data))


def slack_file_upload(filepath, channel, text, token=None, client=None):
    if token is None and client is None:
        raise ValueError("Both token and client are None.")

    import slack

    if client is None:
        t = is_file_or_raw_text(token)
        # make slack client
        client = slack.WebClient(token=t)

    c = is_file_or_raw_text(channel)

    # file upload
    client.files_upload(channels=c, file=filepath, initial_comment=text)
