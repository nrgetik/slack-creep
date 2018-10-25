# slack-creep
Attempts to discover and notify when a particular user (or users) sends
a message in any (accessible) Slack channel

## Usage
```Usage: slack-creep.py [OPTIONS]

Options:
  -t, --token <token>  Slack API Token  [required]
  -u, --users <users>  Single or comma-separated list of users to alert on
                       [default: slackbot]
  -a, --age <age>      Maximum age, in seconds, of messages that are relevant.
                       Will also determine the sleep value between groups of
                       searches  [default: 60]
  -s, --speak          Set this flag if you want notifications to speak to you
                       [default: False]
  -d, --debug          Enable debug output  [default: False]
  --help               Show this message and exit.
```

### Notes
The `say` and `afplay` commands are only available on OS X. This could easily
be adapted to use equivalent commands on other platforms.
