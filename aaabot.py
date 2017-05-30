import os
import time
import re
import pandas as pd
from slackclient import SlackClient


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
RUSSIA_REGEX="(\s+)?(set russia)(\W)(\w+)"
GERMANY_REGEX="(\s+)?(set germany)(\W)(\w+)"
UK_REGEX="(\s+)?(set uk)(\W)(\w+)"
JAPAN_REGEX="(\s+)?(set japan)(\W)(\w+)"
USA_REGEX="(\s+)?(set usa)(\W)(\w+)"
SIDES=['Russia', 'Germany', 'UK', 'Japan', 'USA']

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def get_status(df):
    status = ""
    for country in SIDES:
        status += country + " " + str(df.iloc[0][country]) + "\n"

    return status

def handle_command(command, channel):
    response = "Not sure what you mean by " + command
    df = pd.read_csv("bank.csv")
    print(df)

    if re.match(RUSSIA_REGEX, command):
        value = re.match(RUSSIA_REGEX, command).group(4)
        df.set_value(0,'Russia', value)
        response = get_status(df)
    elif re.match(GERMANY_REGEX, command):
        value = re.match(GERMANY_REGEX, command).group(4)
        df.set_value(0,'Germany', value)
        response = get_status(df)
    elif re.match(UK_REGEX, command):
        value = re.match(UK_REGEX, command).group(4)
        df.set_value(0,'UK', value)
        response = get_status(df)
    elif re.match(JAPAN_REGEX, command):
        value = re.match(JAPAN_REGEX, command).group(4)
        df.set_value(0,'Japan', value)
        response = get_status(df)
    elif re.match(USA_REGEX, command):
        value = re.match(USA_REGEX, command).group(4)
        df.set_value(0,'USA', value)
        response = get_status(df)
    elif re.match("status", command):
        response = get_status(df)

    df.to_csv("bank.csv", index=False)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Axis and Allies Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
