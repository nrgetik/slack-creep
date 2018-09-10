# slack-creep
Attempts to discover and notify when a particular user (or users) sends
a message in any (accessible) channel

## Usage
```Usage: slack-creep.py [OPTIONS]

Options:
  -t, --token <token>  Slack API Token  [required]
  -u, --users <users>  Single or comma-separated list of users to alert on
                       [default: slackbot]
  -a, --age <age>      Maximum age, in seconds, of messages that are relevant.
                       Will also determine the sleep value between groups of
                       searches  [default: 60]
```

### Notes
The `say` command is only available on OS X. If you want to run this on
Linux, comment those lines out or adapt the `say` function to use e.g.
`espeak`