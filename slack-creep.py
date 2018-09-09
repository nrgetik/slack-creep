#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import requests
from os import system
from subprocess import call
from sys import exit
from time import sleep, time

USERS = ['slackbot']

@click.command()
@click.option("-t", "--token", is_flag=False, type=click.STRING,
              metavar="<token>", required=True, help="Slack API Token")
@click.option("-u", "--users", is_flag=False, default=','.join(USERS),
              show_default=True, type=click.STRING, metavar="<users>",
              help="Single or comma-separated list of users to alert on")
@click.option("-a", "--age", is_flag=False, default=60, show_default=True,
              type=click.INT, metavar="<age>",
              help="Maximum age, in seconds, of results we care about. " \
              "Will also determine the sleep value between search clusters")
def main(token, users, age):
    users = [u.strip() for u in users.split(",")]
    try:
        while True:
            for user in users:
                payload = {"token": token,
                           "query": "from:@{}".format(user),
                           "count": 1,
                           "sort": "timestamp"}
                r = requests.get("https://slack.com/api/search.messages",
                                 params=payload)
                if r.status_code != requests.codes.ok:
                    r.raise_for_status()
                else:
                    match_ts = float(r.json()["messages"]["matches"][0]["ts"])
                    if time()-age-5 < match_ts < time():
                        print("{}\n{}\n#{} // @{}: {}".format(
                             "-"*80,
                             r.json()["messages"]["matches"][0]["permalink"],
                             r.json()["messages"]["matches"][0]["channel"]["name"],
                             r.json()["messages"]["matches"][0]["username"],
                             r.json()["messages"]["matches"][0]["text"]))
                        call(["say", "-v", "Daniel", "Greetings; {} has said a thing in {}".format(
                            r.json()["messages"]["matches"][0]["username"],
                            r.json()["messages"]["matches"][0]["channel"]["name"]
                        )])
                sleep(0.125)
            sleep(age)
    except KeyboardInterrupt:
        exit(0)
        

if __name__ == "__main__":
    main()
