import json
import os

import requests

from esa_unfurl.esa import EsaPage


def main(event, context):
    if "body" in event.keys():
        body = json.loads(event["body"])
        if "challenge" in body.keys():
            return body["challenge"]
        else:
            unfurls = dict()

            for link in body["event"]["links"]:
                ep = EsaPage.request(link["url"], os.environ["ESA_TOKEN"])
                unfurls[ep.url] = ep.to_attachment()

            headers = {"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"}
            payload = {
                "token": os.environ["SLACK_TOKEN"],
                "channel": body["event"]["channel"],
                "ts": body["event"]["message_ts"],
                "unfurls": unfurls,
            }
            r = requests.post("https://slack.com/api/chat.unfurl", json=payload, headers=headers)
    return ""