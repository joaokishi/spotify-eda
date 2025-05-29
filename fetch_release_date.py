import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# === SET YOUR CREDENTIALS HERE ===
client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
df=pd.read_csv("SpotifyFeatures.csv")
df_sorted = df.sort_values(['genre', 'popularity'], ascending=[True, False])
top_20_per_genre = df_sorted.groupby('genre').head(20).reset_index(drop=True)
# Authenticate to Spotify API
def fetch_release_date(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    try:
        result = sp.search(q=query, type='track', limit=1)
        items = result['tracks']['items']
        if items:
            album = items[0]['album']
            return album['release_date']
        else:
            return None
    except Exception as e:
        print(f"Error for '{track_name}' by '{artist_name}': {e}")
        return None

release_dates = []

print("Fetching release dates, please wait...")

total = len(top_20_per_genre)
for idx, row in top_20_per_genre.iterrows():
    rd = fetch_release_date(row['track_name'], row['artist_name'])
    release_dates.append(rd)
    print(f"[{idx+1}/{total}] '{row['track_name']}' by '{row['artist_name']}' -> {rd}")
top_20_per_genre['release_date'] = release_dates
top_20_per_genre.to_csv('spotify_with_release_dates.csv', index=False)
print("\nFinished fetching release dates.")
print(top_20_per_genre)
