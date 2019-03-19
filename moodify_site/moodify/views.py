# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django import forms

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

import tweepy

class UserName(forms.Form):
  name = forms.CharField(label='Username', max_length=40)

def get_tweets(request):
  if 'Username' in request.GET:
    uname = request.GET['Username']
    
    consumer_key = "ckWshdUaNqkODubT0ud1aYTwZ"
    consumer_secret = "aBahFPcKiAFuH6UnyY1RS1TCPHpUZTAiDqutfROjQC4h1L20Bp"
    access_key = "354408891-XPtSKVLf38W2ECToclWdPpL3FwjUVJAmvecILDLU"
    access_secret = "Guh9GvZCRC76jDwx8rTskVhlZHnB5JMXFdc6KPD4mYql8"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    new_tweets = api.user_timeline(screen_name=uname, tweet_mode="extended")
    return render(request, 'tweet_results.html', {'uname': uname, 'tweets': new_tweets})
  
  else:
    message = 'Empty Form'
  
  return HttpResponse(message)


@ensure_csrf_cookie
def index(request):
    return render_to_response('index.html')