# smile-cycle
Bot to cycle 

Tutorial can be found [here](https://www.twilio.com/blog/2017/12/facebook-messenger-bot-python.html)

### Getting started:
Run the following to get started

#### Prepare python2
- `brew install python2`
- `pip2 install Flask==0.12.2`
- `pip2 install pymessenger==0.0.7.0`

#### Run your server
- `python2 main.py`
  - Test by connecting to http://127.0.0.1:5000

#### Install ngrok and expose app 
- `brew install node`
- `npm i -g ngrok`
- `python2 main.py` and `ngrok http 5000`
- Get the address for 5000 (such as https://9011ccc6.ngrok.io) and try that in your browser

#### Hookup on facebook 
Now that we have this running, you can hook this up to facebook and should be able to message the app
