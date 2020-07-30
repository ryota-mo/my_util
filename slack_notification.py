import os
import json
import requests
import slack


def is_file_or_raw_text(_input):
    if os.path.isfile(_input):
        # if input is file, read file
        with open(_input, 'r') as f:
            output = f.read().rstrip('\n')
    elif os.path.isdir(_input):
        raise IsADirectoryError(f"Have to input file or text, but you input {_input}")
    else:
        output = _input
    return output


def slack_notification(text, webhook_url, username=None, **kwargs):
    webhook_url = is_file_or_raw_text(webhook_url)
    data = {'text': text, 'link_names': 1}
    if username:
        data.update({'username': username})
    if kwargs:
        data.update(kwargs)

    requests.post(webhook_url, data=json.dumps(data))


def slack_file_upload(filepath, token, channel, message=__file__, client=None):
    """
    Slack Notification
    params: filepath: file sended
    params: token: token strings or text file including token
    params: channel: chennel ID strings or text file including chennel ID
    """
    if token is None and client is None:
        raise ValueError("Both token and client are None.")

    if client is None:
        t = is_file_or_raw_text(token)
        # make slack client
        client = slack.WebClient(token=t)

    c = is_file_or_raw_text(channel)

    # file upload
    client.files_upload(channels=c, file=filepath, initial_comment=message)
