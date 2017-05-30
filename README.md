A Slack bot that I wrote to keep track of each team's balance in Axis and Allies so that we don't have to use pen and paper.

Uses Pandas to read from a one line CSV, which is definitely overkill.

BOT_ID and SLACK_BOT_TOKEN are environment variables for security reasons.

Commands are "@aaabot status" and "@aaabot set [side]", where the sides are Russia, Germany, UK, Japan, and USA.

There's a 0% chance that this will be useful to anyone but my team.
