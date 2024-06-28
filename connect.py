import json
from mattermostdriver import Driver
import config
import requests

from mongo_connect import insert

from llmutils import run

# Map for responses
responses = {}

mattermost_url = "http://localhost:8065"

driver = Driver({
    'url': 'localhost',
    'token': config.bot_token,  # the bot's token
    'scheme': 'http',  # localhost uses http
    'basepath': '/api/v4',
    'verify': False,
    'timeout': 30
})

print(config.bot_token)
driver.login()

# Will change to generalize users
bot_user_id = driver.users.get_user_by_username('snowsidebot')['id']
print(bot_user_id)
my_user_id = driver.users.get_user_by_username('joshuakave')['id']
print(my_user_id)

async def my_event_handler(text):  
    message=json.loads(text)
    if 'data' in message and 'post' in message['data']:
        post_data = json.loads(message['data']['post'])
        if post_data['user_id'] == bot_user_id:
            return
        responses[post_data['user_id']] = post_data['message']
        insert(post_data)
        driver.websocket.disconnect()
    
driver.init_websocket(my_event_handler)

# MATCH PEOPLE HERE AND SEND MESSAGES
# CALL LLM

matches, greetings = run()

print(greetings)

headers = {
    "Authorization": f"Bearer {config.bot_token}",
    "Content-Type": "application/json"
}

count = 0

for match in matches:
    print(match)
    if " " not in match[0]:
        count+=1
        payload = {
        "team_id": "do71aqeuxbnqmr5szcqphygugo",  # The team ID where the channel will be created
        "name": "group_channel_name" + str(count),  # The name of the channel
        "display_name": "Snowside Chat!",
        "type": "P"  # "P" for private, "O" for public
        }
        create_channel_url = f"{mattermost_url}/api/v4/channels"
        response = requests.post(create_channel_url, headers=headers, json=payload)
        channel_data = response.json()
        channel_id = channel_data.get("id")
        add_user_url = f"{mattermost_url}/api/v4/channels/{channel_id}/members"

        for user_id in match:
            add_user_payload = {
                "user_id": user_id
            }
            response = requests.post(add_user_url, headers=headers, json=add_user_payload)
        driver.posts.create_post({
            'channel_id': channel_id,
            'message': greetings[count-1]
        })
        # driver.channels.create_group_message_channel(match)

driver.logout()