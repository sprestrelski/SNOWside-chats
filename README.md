# SNOWside Chats ❄️

## Local Mattermost Docker Setup
[Tutorial](https://docs.mattermost.com/install/install-docker.html) 

### Postgres 
[Tutorial](https://docs.mattermost.com/install/prepare-mattermost-database.html)  

@peterchwl Notes:
- I used brew and simply did brew install postgresql —> this gives you postgresql@14
- Then run createdb:
```bash
createdb
```
- For some reason it didn't make the postgresql user so I used rootuser and it was fine
```bash
sudo -u peter.lee psql
\c postgres # this changes the channel
```
- Then keep following tutorial, don’t need to do step 8
- KEEP PASSWORDS THE SAME “mmuser-password” --> this way you won't have to touch any configs in .env
- Hopefully these steps won't be relevant once Sam gets the shared Postgres running

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

## Mattermost setup
To connect to the Mattermost instance from another device on the network, on the device running the instance, run `ifconfig` and look for an IPV4 address. It should be in the form XXX.XXX.X.XX or similar. Then, go to `XXX.XXX.X.XX:8065` on the secondary device.

## MATTERMOSTDRIVER
1. The mattermostdriver needs to be installed on a venv
2. I named my venv “env” and it’s in the root directory of the repo: python3 -m venv env
3. Then: source env/bin/activate
4. Then, if encountering “No module named pip3”, you need to rollback your pip3 version: python -m ensurepip --default-pip
5. Then you’re able to run: pip3 install mattermostdriver

## IF RUNNING INTO AUTHENTICATION ERRORS:
- curl -i -d '{"login_id":"(your email here)","password":"(your password here)"}' http://localhost:8065/api/v4/users/login
- Replace the login id and password with ur own

## Python setup
Make a `config.py` with the following
```
bot_token = <sample bot token string>
```
