#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
from time import localtime, sleep, strftime, time
import requests
import click
import sys

USERS = ['slackbot']


def dt_stamp():
    return strftime("[%Y-%m-%d %H:%M:%S]", localtime())


def notify(words, speak):
    if speak:
        call(["say", "-v", "Daniel", words])
    else:
        call(["afplay", "/System/Library/Sounds/Glass.aiff"])


@click.command()
@click.option("-t", "--token", is_flag=False, type=click.STRING, metavar="<token>", required=True,
              help="Slack API Token")
@click.option("-u", "--users", is_flag=False, default=','.join(USERS), show_default=True,
              type=click.STRING, metavar="<users>",
              help="Single or comma-separated list of users to alert on")
@click.option("-a", "--age", is_flag=False, default=60, show_default=True, type=click.INT,
              metavar="<age>", help="Maximum age, in seconds, of messages that are relevant. " \
              "Will also determine the sleep value between groups of searches")
@click.option("-s", "--speak", is_flag=True, default=False, show_default=True, type=click.BOOL,
              help="Set this flag if you want notifications to speak to you")
@click.option("-d", "--debug", is_flag=True, default=False, show_default=True, type=click.BOOL,
              help="Enable debug output")
def main(token, users, age, speak, debug):
    users = [u.strip() for u in users.split(",")]
    then_pad = 12
    now_pad = 5
    while True:
        try:
            for user in users:
                payload = {"token": token,
                           "query": "from:@{}".format(user),
                           "count": 1,
                           "sort": "timestamp"}
                response = requests.get("https://slack.com/api/search.messages", params=payload)
                if response.status_code != requests.codes.ok:
                    print("{} Status code error: {}".format(dt_stamp(), response.status_code))
                    sleep(age)
                else:
                    if not response.json()["ok"]:
                        print("{} Response error: {}".format(dt_stamp(), response.json()["error"]))
                        sleep(age)
                    elif response.json()["messages"]["total"] > 0:
                        match = response.json()["messages"]["matches"][0]
                        match_ts = float(match["ts"])
                        now = time()
                        then = now - age - then_pad
                        now = now + now_pad
                        if then <= match_ts <= now and match["channel"]["is_channel"]:
                            print("{}\n{}\n#{} // @{} [{}]: {}".format(
                                "-"*80,
                                match["permalink"],
                                match["channel"]["name"],
                                match["username"],
                                strftime("%H:%M:%S", localtime(match_ts)),
                                match["text"]))
                            if debug:
                                print("DEBUG: {} <= {} <= {}".format(
                                    strftime("%H:%M:%S", localtime(then)),
                                    strftime("%H:%M:%S", localtime(match_ts)),
                                    strftime("%H:%M:%S", localtime(now))))
                            notify("Greetings; {} has said a thing in {}".format(
                                match["username"], match["channel"]["name"]), speak)
            sleep(age)
        except KeyboardInterrupt:
            sys.exit(0)
        # except requests.exceptions.RequestException as exception:
        except Exception as exception:
            print("{} Exception: {} at line {}".format(
                dt_stamp(), exception, sys.exc_info()[2].tb_lineno))
            sleep(age)


if __name__ == "__main__":
    main()
