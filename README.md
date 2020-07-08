# signal-cli-rest-api
signal-cli-rest-api is a wrapper around [signal-cli](https://github.com/AsamK/signal-cli) and allows you to interact with it through http requests.

## Features
* register/verify/unregister a number
* send messages to multiple users/a group with one or multiple attachments
* receive messages (with attachments)
* block/unblock users and groups
* link to existing device
* list/create/update/leave groups
* update profile (name/avatar)

## To-Do
* integrate dbus daemon for faster sending
* authentication

## Installation

### pip

If you install signal-cli-rest-api through pip you need to manually install [signal-cli](https://github.com/AsamK/signal-cli) on your system.

```console
# by default the app will look for the signal config files in ~/.local/share/signal-cli
# you can change the directory by setting the SIGNAL_CONFIG_PATH env var to the desired path
# e.g. export SIGNAL_CONFIG_PATH=/opt/signal
pip install signal-cli-rest-api
uvicorn signal_cli_rest_api.app.main:app --host 0.0.0.0 --port 8000
```

### Docker

```console
export SIGNAL_DATA_DIR=~/signal/
docker run --name signal --restart unless-stopped -p 8000:8000 -v $SIGNAL_DATA_DIR:/root/.local/share/signal-cli sebastiannoelluebke/signal-cli-rest-api
```

### docker-compose
```console
git clone https://github.com/SebastianLuebke/signal-cli-rest-api.git
cd signal-cli-rest-api
# docker-compose build
docker-compose up -d
```

## Security Notice
signal-cli-rest-api doesn't have any authentication for now. Everyone who knows the service address+port and the number is able to get your messages and send messages. So only use it a trusted environment and block external access.

## Interactive Documentation

After installing signal-cli-rest-api start it and open the following page [http://localhost:8000/docs](http://localhost:8000/docs)

