from dotenv import load_dotenv
import os

# https://www.youtube.com/watch?v=WAmEZBEeNmg
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print (CLIENT_ID, CLIENT_SECRET)

# https://www.youtube.com/watch?v=olY_2MW4Eik
import requests
from flask import Flask, redirect, request, jsonify, session, url_for, render_template, send_from_directory
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import urllib.parse
from datetime import datetime
# from scripts.calculate_total import *


app = Flask(__name__)
app.secret_key = CLIENT_SECRET

REDIRECT_URI = 'http://localhost:5000/callback'
# AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
SCOPE = 'user-read-private user-read-email user-top-read'

CACHE_HANDLER = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    scope = SCOPE,
    cache_handler= CACHE_HANDLER,
    show_dialog = True # omit later, used for testing
)

sp = Spotify(auth_manager = sp_oauth)

@app.route('/index')
@app.route('/')
def index():
    logged_in = False 
    # preventing depreciation (I think) according to oauth2.py
    if sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
      logged_in = True
      # not redirecting to auth so page can have a login button and display purpose of site eventually before login
    return render_template('index.html', logged_in = logged_in)  

@app.route('/login')
def login():
    if not sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('index'))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    # this leads to a depreciation warning, but the save_token_to_cache method expects a dictionary so I genuinely 
    # have no clue why get_access_token is tweaking to get me to let it return just 'access_token' when I need the other info
    token_info = sp_oauth.get_access_token(code)
    sp_oauth.cache_handler.save_token_to_cache(token_info)
    return redirect(url_for('index'))

@app.route('/playlists')
def get_playlists():
    if not sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    user = sp.current_user()
    username = user['display_name']
    current_user_playlists = sp.current_user_playlists()
    playlists_info = [{
        'name': playlist_item['name'], 
        'url': playlist_item['external_urls']['spotify'], 
        'images': playlist_item['images'] if playlist_item['images'] else ''
    } for playlist_item in current_user_playlists['items']]
    
    data = {
        'username': username,
        'playlists_info': playlists_info
    }

    return render_template('playlists.html', data = data)

@app.route('/playlist-creator')
def playlist_creator():
    if not sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    user = sp.current_user()
    username = user['display_name']
    current_user_playlists = sp.current_user_playlists()
    playlists_info = [{
        'name': playlist_item['name'], 
        'url': playlist_item['external_urls']['spotify'], 
        'images': playlist_item['images'] if playlist_item['images'] else ''
    } for playlist_item in current_user_playlists['items']]
    
    data = {
        'username': username,
        'playlists_info': playlists_info
    }
    
    return render_template('playlist_creator.html', data = data)

@app.route('/profile')
def get_profile():
    if not sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    user = sp.current_user()
    username = user['display_name']
    user_country = user['country']
    user_follower_count = user['followers']['total']
    user_profile_link = user['href']
    user_profile_image = user['images'][0]['url']

    return render_template('profile.html', username=username, user_country=user_country, user_follower_count=user_follower_count, user_profile_link=user_profile_link, user_profile_image=user_profile_image)

@app.route('/get_top_items', methods=['POST'])
def get_top_items():
    if not sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    data = request.json
    item_type = data.get('item_type')
    limit = data.get('limit', 10)
    time_range = data.get('time_range', 'medium_term')

    if item_type == 'tracks':
        top_items = sp.current_user_top_tracks(limit = limit, time_range = time_range)['items']
    elif item_type == 'artists':
        top_items = sp.current_user_top_artists(limit = limit, time_range = time_range)['items']
    else:
        return jsonify({'error': 'Invalid item type'}), 400

    top_items_info = [{
        'name': item['name'],
        'url': item['external_urls']['spotify'],
        'images': item['images'] if item_type == 'artists' else item['album']['images']
    } for item in top_items]

    return jsonify(top_items_info)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# CONTINUE
# https://www.youtube.com/watch?v=2if5xSaZJlg