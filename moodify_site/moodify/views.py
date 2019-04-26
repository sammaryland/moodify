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

from recommender.api import Recommender

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
    request.session['results'] = results

    return render(request, 'tweet_results.html', {'uname': uname, 'tweets': new_tweets, 'results': results})
  
  else:
    message = 'Empty Form'
  
  return HttpResponse(message)

def recommend_songs(artist, danceability, energy, valence):
  recommender = Recommender()
  recommender.artists = artist
  recommender.limit = 10
  recommender.track_attributes = {
      'max_danceability': danceability,
      'max_energy': energy,
      'max_valence': valence
  }

  return recommender.find_recommendations()

def view_playlist(request):
  if 'Artist' in request.GET:
    artist = request.GET['Artist']
    d = request.session['results']
    analyticalScore = 0
    angerScore = 0
    confidentScore = 0
    disgustScore = 0
    fearScore = 0
    joyScore = 0
    sadnessScore = 0
    tentativeScore = 0

    if 'Analytical' in d:
      analyticalScore = d['Analytical']

    if 'Joy' in d:
      joyScore = d['Joy']

    if 'Confident' in d:
      confidentScore = d['Confident']

    if 'Sadness' in d:
      sadnessScore = d['Sadness']

    if 'Anger' in d:
      angerScore = d['Anger']

    if 'Tentative' in d:
      tentativeScore = d['Tentative']

    if 'Fear' in d:
      fearScore = d['Fear']

    if 'Disgust' in d:
      disgustScore = d['Disgust']

    valence = 0
    if (joyScore > sadnessScore):
      valence = joyScore - sadnessScore
    else:
      valence = sadnessScore - joyScore

    dPositive = ((confidentScore * 4) + (joyScore * 6)) / 10
    dNegative = ((tentativeScore * 3) + (fearScore * 7)) / 10
    danceability = 0

    ePositive = ((joyScore * 8) + (analyticalScore * 2))/10
    eNegative = ((disgustScore * 3) + (sadnessScore * 7))/10
    eBonus = 0
    energy = 0
    if (angerScore > 0.2):
      eBonus = angerScore * 2

    if (dPositive > dNegative):
      danceability = dPositive - dNegative
    else:
      danceability = (1 - dNegative) + dPositive

    if (ePositive > eNegative):
      energy = ePositive - eNegative + eBonus
    else:
      energy = (1 - eNegative) + ePositive + eBonus

    if (energy > 1):
      energy = 1

    songs = recommend_songs(artist, danceability, energy, valence)
    
    return render(request, 'view_playlist.html', {'songs': songs['tracks']})


@ensure_csrf_cookie
def index(request):
    return render_to_response('index.html')

# emotion - anger, disgust, fear, joy and sadness
# language syles - analytical, confident and tentative