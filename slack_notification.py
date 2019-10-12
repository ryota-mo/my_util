import json
import requests


def slack_notification(text, webhook_url, username=None, **kwargs):
    data = {'text': text, 'link_names': 1}
    if username:
        data.update({'username': username})
    if kwargs:
        data.update(kwargs)

    requests.post(webhook_url, data = json.dumps(data))


def slack_file_upload(filepath, channel, text, token=None, client=None):
    if token == None and client == None:
        raise ValueError("Both token and client are None.")

    import slack

    if client != None:
        client = client
    else:
        # make slack client
        client = slack.WebClient(token=token)

    if os.path.isfile(channel):
        # if channel is file, read file
        with open(channel, 'r') as f:
            c = f.read().rstrip('\n')
    else:
        # else, channel is raw channel
        c = channel

    # file upload
    client.files_upload(channels=c, file=filepath, initial_comment=text)
