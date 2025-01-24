from flask import Flask, request, redirect, url_for, session, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_COOKIE_NAME'] = 'spotify_session'

# Spotify OAuth setup
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-top-read user-read-recently-played playlist-modify-public"
)

# Helper function to get Spotify client
def get_spotify_client():
    """Get an authenticated Spotify client with error handling."""
    try:
        token_info = session.get('token_info', None)
        if not token_info:
            logger.warning("No token info found in session")
            return None

        if sp_oauth.is_token_expired(token_info):
            logger.info("Token expired, attempting refresh")
            try:
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['token_info'] = token_info
            except Exception as e:
                logger.error(f"Error refreshing token: {str(e)}")
                return None

        sp = spotipy.Spotify(auth=token_info['access_token'])
        # Test the client with a simple API call
        sp.current_user()  # This will raise an exception if the token is invalid
        return sp
    except Exception as e:
        logger.error(f"Error in get_spotify_client: {str(e)}")
        return None

@app.route('/')
def index():
    """Home route to authenticate user."""
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    """Handle Spotify OAuth callback."""
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('dashboard'))

@app.route('/test-token')
def test_token():
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "Token is invalid or expired"})
    return jsonify({"message": "Token is valid"})

@app.route('/dashboard')
def dashboard():
    sp = get_spotify_client()
    if not sp:
        return redirect('/')

    top_tracks = sp.current_user_top_tracks(limit=10)
    top_artists = sp.current_user_top_artists(limit=10)

    return render_template(
        'dashboard.html',
        top_tracks=[
            {
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "album": track['album']['name'],
                "image": track['album']['images'][0]['url']
            }
            for track in top_tracks['items']
        ],
        top_artists=[
            {
                "name": artist['name'],
                "image": artist['images'][0]['url'] if artist['images'] else None
            }
            for artist in top_artists['items']
        ]
    )

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    """Create a playlist based on user's top tracks."""
    sp = get_spotify_client()
    if not sp:
        return redirect('/')

    # Fetch user ID
    user_id = sp.current_user()['id']

    # Create a new playlist
    playlist_name = "My Top Tracks Playlist"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)

    # Get user's top tracks and add to playlist
    top_tracks = sp.current_user_top_tracks(limit=10)
    track_uris = [track['uri'] for track in top_tracks['items']]

    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

    return jsonify({"message": f"Playlist '{playlist_name}' created successfully!", "playlist_url": playlist['external_urls']['spotify']})

@app.route('/recently_played')
def recently_played():
    """Render recently played tracks."""
    sp = get_spotify_client()
    if not sp:
        return redirect('/')

    recently_played_ = sp.current_user_recently_played(limit=10)
    tracks = [
        {
            "track": item['track']['name'],
            "artist": item['track']['artists'][0]['name'],
            "image": item['track']['album']['images'][2]['url'],  # Small image
        }
        for item in recently_played_['items']
    ]

    # Pass data to the template
    return render_template(
        'recently_played.html',
        recently_played=tracks
    )


if __name__ == '__main__':
    app.run(debug=True, port=8080)