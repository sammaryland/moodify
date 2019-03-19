# Moodify
#### Sam Maryland, Taylor Wilson, Amanda Holloman

Install Virtualenv

```
pip install virtualenv
```

Create Virtual Environment

```
virtualenv -p /usr/bin/python2.7 venv2/7
source venv2.7/bin/activate
```

Download Requirements

```
pip install -r moodify_site/requirements.txt
```

Run the Program

```
python moodify_site/manage.py runserver
```

Point your browser to:

```
127.0.0.1:8000
```