#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import requests
from os import system
from subprocess import call
from sys import exit
from time import localtime, sleep, strftime, time

USERS = ['slackbot']


def say(words):
    call(["say", "-v", "Daniel", words])


@click.command()
@click.option("-t", "--token", is_flag=False, type=click.STRING, metavar="<token>", required=True,
              help="Slack API Token")
@click.option("-u", "--users", is_flag=False, default=','.join(USERS), show_default=True,
              type=click.STRING, metavar="<users>",
              help="Single or comma-separated list of users to alert on")
@click.option("-a", "--age", is_flag=False, default=60, show_default=True, type=click.INT,
              metavar="<age>", help="Maximum age, in seconds, of messages that are relevant. " \
              "Will also determine the sleep value between groups of searches")
def main(token, users, age):
    users = [u.strip() for u in users.split(",")]
    mini_sleep = 0.25
    age_pad = len(users) * (mini_sleep * 1.5)
    try:
        while True:
            for user in users:
                payload = {"token": token,
                           "query": "from:@{}".format(user),
                           "count": 1,
                           "sort": "timestamp"}
                r = requests.get("https://slack.com/api/search.messages", params=payload)
                if r.status_code != requests.codes.ok:
                    r.raise_for_status()
                else:
                    if not r.json()["ok"]:
                        print("Error: {}".format(r.json()["error"]))
                        say("Error: {}".format(r.json()["error"]))
                    else:
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
                            say("Greetings; {} has said a thing in {}".format(
                                match["username"], match["channel"]["name"]))
                sleep(mini_sleep)
            sleep(age)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
