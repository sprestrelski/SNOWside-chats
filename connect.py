from mattermostdriver import Driver
import config

driver = Driver({
    'url': 'localhost',
    # 'team': 'general',
    'token': config.bot_token, #the bot's token
    'scheme': 'http', #localhost uses http
    'basepath': '/api/v4',
    'verify': False,
    'timeout': 30
})

driver.login()

channel_id = '9c4qrrrwijrz3r6tq6y5eircxo' #get this by running /api/v4/channels
driver.posts.create_post({
    'channel_id': channel_id,
    'message': 'Hello from my Mattermost bot!'
})

driver.logout()