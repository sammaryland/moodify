# Moodify
Moodify is a Python-based web application which will generate a Spotify playlist based on the tone of a user's tweets. The tweets are retrieved using Tweepy, then sent to the IBM Watson Tone Analyzer for analysis. Based on the results, the user will recieve a Spotify playlist.

## Prerequisites
Update your Twitter and Watson API keys located in config.py
```
moodify_site/moodify/config.py
```

Update your Spotify API keys via command line such as:
```
export SPOTIFY_CLIENT_ID='SPOTIFY_CLIENT_ID'
export SPOTIFY_CLIENT_SECRET='SPOTIFY_CLIENT_SECRET'
```

Install Virtualenv

```
pip install virtualenv
```

Create Virtual Environment

```
virtualenv -p /usr/bin/python2.7 venv2.7
source venv2.7/bin/activate
```

Download Requirements

```
pip install -r moodify_site/requirements.txt
```

## Run the Program

```
python moodify_site/manage.py runserver
```

Point your browser to:

```
127.0.0.1:8000
```

Enter any Twitter username. For the demo, enter 'JessicaGonzo5', then submit.

## Authors
* **Sam Maryland**
* **Taylor Wilson**
* **Amanda Holloman**