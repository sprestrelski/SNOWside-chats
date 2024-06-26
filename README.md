# SNOWside Chats ❄️

## Local Mattermost Docker Setup
[Tutorial](https://docs.mattermost.com/install/install-docker.html) 

### Postgres 
[Tutorial](https://docs.mattermost.com/install/prepare-mattermost-database.html)

### Docker
1. Install Docker Desktop and keep it open.
2. Create a `.env` file and change the `DOMAIN` to `localhost`. 
On Mac: ([source](https://stackoverflow.com/questions/76299173/getting-error-error-getting-credentials-err-exit-status-1-out-when-tr))
> In `~/.docker/config.json`, change `"credsStore" : "desktop"` with `"credsStore": osxkeychain"`
```bash
cd docker
cp env.example .env
```

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

## Mattermost setup
To connect to the Mattermost instance from another device on the network, on the device running the instance, run `ifconfig` and look for an IPV4 address. It should be in the form XXX.XXX.X.XX or similar. Then, go to `XXX.XXX.X.XX:8065` on the secondary device.