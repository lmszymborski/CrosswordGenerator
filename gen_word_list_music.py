import requests
import base64
from secrets import *
import json
import lyricsgenius
import re

# https://prettystatic.com/automate-the-spotify-api-with-python/
def _get(url, args=None, payload=None, **kwargs):
    if args:
        kwargs.update(args)

    return _internal_call("GET", url, payload, kwargs)

def get_id(artist, token):
    url = 'https://api.spotify.com/v1/search?q=' + artist + '&type=artist'
    headers = {"Authorization": "Bearer " + token}
    r = requests.get(url, headers=headers)
    response = r.json()
    return response['artists']['items'][0]['id']

def find_lyrics(artist, song_name):
    song_name = re.sub("[\(\[].*?[\)\]]", "", song_name)
    genius = lyricsgenius.Genius(geniusAccessToken)
    print(artist[0])
    song = genius.search_song(song_name, artist[0])
    print(song.lyrics)

def authorize():
    CLIENT_ID = '0080d98c83ad4577a89e760f264f6561'
    CLIENT_SECRET = '404d18a13b6a47f89c66c045a0068fe1'
    url = 'https://accounts.spotify.com/api/token'
    #data_str = CLIENT_ID + ":" + base64.b64encode(CLIENT_SECRET)

    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers = {"Authorization": "Basic " + base64Message}
    data = {"grant_type": 'client_credentials'}

    r = requests.post(url, headers=headers, data=data)

    response = r.json()
    print(response)
    return response['access_token']
    
def get_artist_tracks(artist_name, token):
    artist_id = get_id(fix_artist_name(artist_name), token)
    country = 'USA'
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/top-tracks?market=ES'
    headers = {"Authorization": "Bearer " + token}
    data = {"country": country}
    r = requests.get(url, headers=headers)
    response = r.json()
    top_tracks = []
    
    for track in response['tracks']:
        #print(track['name'])
        top_tracks.append(track['name'])
        #artists = []
        #for artist in track['artists']:
        #    artists.append(artist['name'])
        #top_tracks[track['name']] = artists
    
    #print(top_tracks)
    return top_tracks
    #print(response)

def fix_artist_name(name):
    name = name.replace(" ", "%2B")
    return name

def main():
    #token = authorize()
    #ariana_id = get_id("Ariana%2BGrande", token)
    #print(artist)
    #tracks = get_artist_tracks("Of Monsters and Men", token)
    print(tracks)
    '''
    for track in tracks:
        #find_lyrics(tracks[track], track)
        find_lyrics(artist, track)
    '''


if __name__ == '__main__':
    main()