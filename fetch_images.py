import datetime
import os
import shutil
import sys

import requests
import spotipy
from random_word import RandomWords
from spotipy.oauth2 import SpotifyOAuth

import helpers


def saved(sp, output_path):
    source = sp.current_user_saved_tracks()
    for saved_track in source['items']:
        curr_name = saved_track['track']['album']["name"]
        curr_url = saved_track['track']['album']["images"][0]['url']

        filename = curr_name + ".png"
        filename = filename.replace(" ", "_")

        r = requests.get(curr_url, stream=True)

        try:
            os.mkdir(output_path)
        except BaseException:
            pass

        if r.status_code == 200:
            r.raw.decode_content = True
            try:
                o = output_path + "/{}".format(filename)
                with open(o, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            except BaseException:
                continue


def the_rest(sp, tracks, tr, output_path):
    if tracks:
        item_list = sp.current_user_top_tracks(time_range=tr)['items']
    else:
        item_list = sp.current_user_top_artists(time_range=tr)['items']
    for item in item_list:
        if tracks:
            curr_name = item['album']["name"]
            curr_url = item['album']["images"][0]['url']
        else:
            curr_name = item['name']
            curr_url = item['images'][0]['url']

        filename = curr_name + ".png"
        filename = filename.replace(" ", "_")

        r = requests.get(curr_url, stream=True)

        try:
            os.mkdir(output_path)
        except BaseException:
            pass

        if r.status_code == 200:
            r.raw.decode_content = True
            try:
                o = output_path + "/{}".format(filename)
                with open(o, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            except BaseException:
                continue


scope = "user-library-read user-top-read"
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
except BaseException:
    # TODO be nice
    print("Log in bitch")
    exit()

f = {
    "s": "short_term",
    "m": "medium_term",
    "l": "long_term",
}


try:
    param = sys.argv[1]

except BaseException:
    print("Usage:\npython3 fetch_images.py saved|tts|ttm|ttl|tas|tam|tal")
    exit()

r = RandomWords()
word = str(r.get_random_word()).lower()
output_path = "./art_{}_{}/".format(param, word)

if sys.argv[1] == "saved":
    saved(sp, output_path)
else:
    the_rest(sp, sys.argv[1][1] == "t", f[sys.argv[1][2]], output_path)

print("Output to :", output_path)
print("Display with command:\npython3 display_images.py \"" + output_path + "\"")
