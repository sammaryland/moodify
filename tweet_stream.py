# Determine the top 10 most popular (mentioned) hashtags 
# within 10 minutes of listening to Twitter public stream 
# GET statuses/sample For each hashtag, print hashtag 
# and number of tweets containing it.

from twitter import *

import oauth2
import urllib2
import json
import operator
import time
from itertools import islice
import string

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(".")
import config

api_endpoint = "https://stream.twitter.com/1.1/statuses/sample.json?include_entities=true"

consumer = oauth2.Consumer(
	key = config.consumer_key,
	secret = config.consumer_secret
)
token = oauth2.Token(
	key = config.access_key,
	secret = config.access_secret
)

signature_method_hmac_sha1 = oauth2.SignatureMethod_HMAC_SHA1()
oauth_request = oauth2.Request.from_consumer_and_token(
  consumer,
  token=token,
  http_method='GET',
  http_url=api_endpoint
)
oauth_request.sign_request(signature_method_hmac_sha1, consumer, token)

hashtag_freq = {}

printable = set(string.printable)

res = urllib2.urlopen(oauth_request.to_url())
start_time = time.ctime()
timeout = time.time() + 10
while True:
  for r in res:
    tweet = json.loads(r)
    if "delete" in tweet:
      continue
    if tweet["user"]["lang"] != "en":
      continue
    if tweet["entities"]["hashtags"] == 0:
      continue
    if len(tweet["entities"]["hashtags"]) != 0:
      t = tweet["text"]
      h = tweet["entities"]["hashtags"][0]["text"]
      filter(lambda x: x in printable, t)
      filter(lambda x: x in printable, h)
      print t + " " + h
      if time.time() > timeout:
        break
  break

sorted_freq = sorted(hashtag_freq.items(), key=operator.itemgetter(1), reverse=True)
end_time = time.ctime()
