# slack-creep
Attempts to discover and notify when a particular user (or users) sends a message in any Slack
channel accessible to the user associated with the specified
[API Token](https://api.slack.com/custom-integrations/legacy-tokens)

## Installation

Something like:

1. `git clone git@github.com:nrgetik/slack-creep.git`
2. `mkvirtualenv slack-creep`
3. `pip install -r requirements.txt`

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

1. This has been developed on and tested with `python3`
2. The `say` and `afplay` commands are only available on OS X. This code could easily be adapted
to use similar utilities available on other platforms
