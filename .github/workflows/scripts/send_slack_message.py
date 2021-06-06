import argparse
import os
import requests


SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK', '')


def send_message(message):

    requests.post(
        url=SLACK_WEBHOOK,
        headers={'Content-type': 'application/json'},
        data={
            "blocks": [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }]
        }
    )


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
