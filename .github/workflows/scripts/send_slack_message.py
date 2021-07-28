import argparse
import json
import os
import requests


SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK', '')


def send_message(message):

    response = requests.post(
        url=SLACK_WEBHOOK,
        headers={'Content-type': 'application/json'},
        data=json.dumps({"text": message})
    )

    if response.status_code != 200:
        print('Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text))


def parse_args():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="slackbot",
        description="DGS Covid19 Slack Bot",
        usage="%(prog)s [options]",
        epilog="Send messages to Slack channel #covid19-repo-updates",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--message",
        type=str,
        default=None,
        help="Slack message."
    )

    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()

    send_message(args.message)
