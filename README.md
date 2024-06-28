# SNOWside Chats ❄️
Want to know your colleagues better? Not sure how to reach out?

Try SNOWside chats! Our premiere software uses ✨generative AI✨ to match you to people with similar interests and set up 1:1s! 

![logo](images/snowside-logo.png)

## How does it work?
SNOWside Chats is a Mattermost bot that matches people within ServiceNow based on your interests. All you need to do is enter a blurb about yourself, and SNOWside's matching algorithm will set up one-on-one's with you and your ServiceNow soulmate!
1. DM the bot with a bio
> Sam: Hi, I'm Sam and I'm an intern on the IntegrationHub team! I'm into crafts and long walks on the beach.  
> Shruti: Hi I'm Shruti! I study computer engineering and love knitting and rollerblading. I'm on the ML QE Team!
2. Set up the 1:1 matching in a channel 
3. Snowside will make channels for each of the matches!
> Hey Sam and Shruti! I'm Snowside, nice to meet you both! It sounds like you both enjoy some great hobbies outside of work/school - Sam, I'm sure your beach walks are amazing, and Shruti, knitting and rollerblading are such cool skills! Why don't you two chat about your favorite crafting projects or outdoor adventures? See where the conversation takes you!

Stack
- Local instance: Mattermost and Postgres
- Bot: Python and MongoDB

All software was created and tested on MacOS, which means things may break on other distributions.

## Mattermost Setup
[Main Tutorial](https://docs.mattermost.com/install/install-docker.html) || [Database Tutorial](https://docs.mattermost.com/install/prepare-mattermost-database.html)

We'll set up the Postgres database and Docker instance first, then the bot itself.

### Postgres  
Install postgresql 
```bash
brew install postgresql # this installs postgresql@14
```
Then run createdb:
```bash
createdb
```

If this doesn't make the postgresql user, use rootuser
```bash
sudo -u peter.lee psql
\c postgres # this changes the channel
```
Then, follow the rest of the database setup tutorial.


### Docker
1. Install Docker Desktop and keep it open.
2. Create a `.env` file and change the `DOMAIN` to `localhost`. Also, change `MATTERMOST_IMAGE=mattermost-enterprise-edition` to `MATTERMOST_IMAGE=mattermost-team-edition` since the teams edition is free.
```bash
cd docker
cp env.example .env
```

On Mac: ([source](https://stackoverflow.com/questions/76299173/getting-error-error-getting-credentials-err-exit-status-1-out-when-tr))
> In `~/.docker/config.json`, change `"credsStore" : "desktop"` with `"credsStore": osxkeychain"`

This fixes the error
> error getting credentials - err: exit status 1, out: ``


3. Change permissions so Docker can access files
```bash
mkdir -p ./volumes/app/mattermost/{config,data,logs,plugins,client/plugins,bleve-indexes}
sudo chown -R 2000:2000 ./volumes/app/mattermost
sudo chmod 777 ./volumes/app/mattermost/config
```
4. Use the docker command without the included NGINX. 
```bash
sudo docker compose -f docker-compose.yml -f docker-compose.without-nginx.yml up -d
```
to shut down
```bash
sudo docker compose -f docker-compose.yml -f docker-compose.without-nginx.yml down
```

This will run the Mattermost instance on port 8065 and the postgres database on port 5432.

### Connecting from other devices
To connect to the Mattermost instance from another device on the network, on the device running the instance, run `ifconfig` and look for an IPV4 address. It should be in the form XXX.XXX.X.XX or similar. Then, go to `XXX.XXX.X.XX:8065` on the secondary device.


## Bot Setup

1. Create a virtual environment and activate it
```bash
python3 -m venv env
source env/bin/activate
```
2. Install dependencies
```bash
pip3 install mattermostdriver langchain ollama pandas numpy
```
3. Make a `config.py` with the following
```
bot_token = <sample bot token string>
mongo_uri = <sample mongo uri>
```
4. Run `python3 connect.py` to start the bot!

### Debugging
If encountering “No module named pip3”
- You need to rollback your pip3 version: `python -m ensurepip --default-pip`

If running into authentication issues,
- curl -i -d '{"login_id":"(your email here)","password":"(your password here)"}' http://localhost:8065/api/v4/users/login
- Replace the login id and password with your own
