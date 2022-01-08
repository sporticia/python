#!/usr/bin/python

import boto3
from botocore.exceptions import ClientError
import datetime
import json
import requests

secrets_manager_client = boto3.client('secretsmanager')
ssm_client             = boto3.client('ssm')

def get_slack_token():
    keys = {}
    try:
        # paramstore Slack App oAuth token
        key_name = "<slack-oauth-token>"
        r = ssm_client.get_parameter(
            Name=key_name,
            WithDecryption=True
        )
        keys['<slack-oauth-token>'] = r['Parameter']['Value']
        return keys['<slack-oauth-token>']
    except Exception as e:
        print(e)

def slack_post_message(user, subject):
    webhook_url = 'https://hooks.slack.com/services/<slack-webhook-url>'
    slack_token = get_slack_token()
    slack_user_name = 'UserName'
    slack_text = 'Slack message'

    try:
        r = requests.post(webhook_url, headers={'Authorization': 'Bearer ' +slack_token}, data=json.dumps({
            'username': slack_user_name,
            'text': slack_text
        }))
        r.raise_for_status()
        if r.status_code == 200:
          print("Message posted")

    except requests.exceptions.HTTPError as e:
        print (e.response.text)


slack_post_message("name", "subject")

