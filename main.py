import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load credentials from .env file
load_dotenv()

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-modify-public user-library-read"
))

# Function to search for a song by its name and retrieve the track ID
def get_track_id(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        return tracks[0]['id']
    else:
        print(f"❌ Song '{song_name}' not found.")
        return None

# Get the user ID
try:
    user_id = sp.current_user()["id"]
except spotipy.exceptions.SpotifyException as e:
    print(f"❌ Error fetching user info: {e}")
    exit()

# Create a playlist
playlist_name = input("Enter a name for your playlist: ").strip() 
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
playlist_id = playlist["id"]

# List to store the track IDs
track_ids = []

# Loop to add tracks by song name
while True:
    song_name = input("Enter a song name to add to the playlist (or 'done' to finish): ").strip()
    if song_name.lower() == 'done':
        break

    track_id = get_track_id(song_name)
    if track_id:
        track_ids.append(track_id)

# Add the tracks to the playlist
if track_ids:
    try:
        sp.playlist_add_items(playlist_id, track_ids) 
        print(f"✅ Playlist '{playlist_name}' created and tracks added!") 
        print(f"🔗 Playlist URL: {playlist['external_urls']['spotify']}")
    except Exception as e:
        print(f"❌ Error adding tracks to the playlist: {e}")
else:
    print("❌ No tracks were added to the playlist.")
