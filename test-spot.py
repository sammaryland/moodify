from recommender.api import Recommender
import spotipy

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

client_credentials_manager = SpotifyClientCredentials(client_id='e107bb5ac5f848998e41dfdab61de8f7', client_secret='c61b8824504a438595b1e67ab0be0194')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if __name__ == '__main__':

    recommender = Recommender()
    recommender.artists = 'The Beatles'
    recommender.limit = 10
    recommender.track_attributes = {
        'max_danceability': 0.5,
        'min_energy': 0.5,
        'min_valence': 0.5
    }

    recommendations = recommender.find_recommendations()
    for recommendation in recommendations['tracks']:
        print("%s - %s" % (recommendation['name'], recommendation['artists'][0]['name']))

    p = []
    for recommendation in recommendations['tracks']:
        p.append(recommendation['uri'][14:])
    
    print p

# {u'Tentative': 0.7825817500000001, u'Joy': 0.836431375, u'Confident': 0.849827, u'Sadness': 0.66027825, u'Anger': 0.679817, u'Analytical': 0.620279}
