#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import requests
from os import system
from subprocess import call
from sys import exc_info, exit
from time import localtime, sleep, strftime, time

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
def main(token, users, age, speak):
    users = [u.strip() for u in users.split(",")]
    mini_sleep = 0.125
    age_pad = max(len(users)*mini_sleep, 5)
    while True:
        try:
            for user in users:
                payload = {"token": token,
                           "query": "from:@{}".format(user),
                           "count": 1,
                           "sort": "timestamp"}
                r = requests.get("https://slack.com/api/search.messages", params=payload)
                if r.status_code != requests.codes.ok:
                    print("{} Status code error: {}".format(dt_stamp(), r.status_code))
                    sleep(age)
                else:
                    if not r.json()["ok"]:
                        print("{} Response error: {}".format(dt_stamp(), r.json()["error"]))
                        sleep(age)
                    elif r.json()["messages"]["total"] > 0:
                        match = r.json()["messages"]["matches"][0]
                        match_ts = float(match["ts"])
                        now = time()
                        if now-age-age_pad <= match_ts <= now and match["channel"]["is_channel"]:
                            print("{}\n{}\n#{} // @{} [{}]: {}".format("-"*80,
                                match["permalink"],
                                match["channel"]["name"],
                                match["username"],
                                strftime("%I:%M %p", localtime(match_ts)),
                                match["text"]))
                            notify("Greetings; {} has said a thing in {}".format(
                                match["username"], match["channel"]["name"]), speak)
                sleep(mini_sleep)
            sleep(age)
        except KeyboardInterrupt:
            exit(0)
        # except requests.exceptions.RequestException as e:
        except Exception as e:
            print("{} Exception: {} at line {}".format(dt_stamp(), e, exc_info()[2].tb_lineno))
            sleep(age)


if __name__ == "__main__":
    main()
