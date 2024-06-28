import json
from mattermostdriver import Driver
import config


from mongo_connect import insert

from llmutils import run



# Map for responses
responses = {}

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

matches = run()

for match in matches:
    print(match)
    if " " not in match[0]:
        print("hello")
        driver.channels.create_group_message_channel(match)

#driver.channels.create_channel

driver.logout()