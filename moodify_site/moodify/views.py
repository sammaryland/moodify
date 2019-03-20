# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import config

from django.shortcuts import render
from django import forms

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

import tweepy
from watson_developer_cloud import ToneAnalyzerV3
import urllib, json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(".")

tone_analyzer = ToneAnalyzerV3(
  iam_apikey=config.watson_api_key,
  version='2017-09-21'
)

class UserName(forms.Form):
  name = forms.CharField(label='Username', max_length=40)

def analyze_tweets(tweets):
  results = {}
  for tweet in tweets:
    json_output = tone_analyzer.tone(tweet.full_text, content_type='text/plain').get_result()
    for i in json_output['document_tone']['tones']:
      n = i['tone_name']
      s = i['score']
      if n not in results:
        results[n] = s
      results[n] = (results[n] + s) / 2
  for k, v in results.items():
    print str(k) + "\t" + str(v)
  return results

def get_tweets(request):
  if 'Username' in request.GET:
    uname = request.GET['Username']

    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_key, config.access_secret)
    api = tweepy.API(auth)

    new_tweets = api.user_timeline(screen_name=uname, count=10, tweet_mode="extended")
    results = analyze_tweets(new_tweets)
    return render(request, 'tweet_results.html', {'uname': uname, 'tweets': new_tweets, 'results': results})
  
  else:
    message = 'Empty Form'
  
  return HttpResponse(message)


@ensure_csrf_cookie
def index(request):
    return render_to_response('index.html')