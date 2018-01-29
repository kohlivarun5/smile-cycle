# smile-cycle
Bot to cycle 

Tutorial can be found [here](https://github.com/yukuku/telebot)

### Create local credentials
The app requires credentials, but we don't want them in git, 
so create a file such as:
- `gvim credentials.py`

```
TELEGRAM_TOKEN='<TOKEN_FROM_BOT_FATHER'
```

### Getting started:
Run the following to get started

#### Prepare python2
- `brew install python2`
- `echo -e "[install]\nprefix=" > ~/.pydistutils.cfg`
- `pip2 install -t lib -r requirements.txt`

#### Setup App-Engine
- Download and install AppEngine from (here)[https://cloud.google.com/appengine/docs/standard/python/download]
- Run the dev server: `dev_appserver.py app.yaml --port 5000 --enable_host_checking false`
  - Visit http://localhost:5000/me

#### Install ngrok and expose app 
- `brew install node`
- `npm i -g ngrok`
- `ngrok http 5000`
- Get the address for 5000 (such as https://9011ccc6.ngrok.io) and try that in your browser

#### Hookup Telegram webhook
- Visit https://9011ccc6.ngrok.io/set_webhook?url=https://9011ccc6.ngrok.io/webhook

#### Deploy
- Deploy the app: `gcloud app deploy` 
- Set the webhook url for PRO
