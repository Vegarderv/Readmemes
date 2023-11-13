import logging
import json
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token="ADD_TOKEN_HERE")
logger = logging.getLogger(__name__)

conversation_history = []
channel_name = "readmemes"
channel_id = "C10LS90JD"
cursor = None


for i in range(100):
    try:
        # Call the conversations.history method using the WebClient
        # conversations.history returns the first 100 messages by default
        # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
        result = client.conversations_history(channel=channel_id, limit=200, cursor=cursor)

        conversation_history += result["messages"]
        if result["response_metadata"] == None:
            break
        cursor = result["response_metadata"]["next_cursor"]

        # Print results
        logger.info("{} messages found in {}".format(len(conversation_history), channel_id))

    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))
        print("Breaking")
        break



with open("messages2.json", "w", encoding="utf8") as f:
    f.write(json.dumps(conversation_history))
