import json
from mattermostdriver import Driver
import config

# Map for responses
responses = {}

driver = Driver({
    'url': 'localhost',
    'token': config.bot_token,  # the bot's token
    'scheme': 'http',  # localhost uses http
    'basepath': '/api/v4',
    'verify': False,
    'timeout': 30,
    'team_id' : config.team_id
})

driver.login()

# Will change to generalize users
bot_user_id = driver.users.get_user_by_username('snowbot')['id']
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

        driver.posts.create_post({
            'channel_id': post_data['channel_id'],
            'message': 'I heard you say: ' + post_data['message'] + ' and stored it in my memory: ' + responses[post_data['user_id']]
        })
        return
    
driver.init_websocket(my_event_handler)

driver.logout()