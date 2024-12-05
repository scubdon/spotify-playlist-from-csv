import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
from typing import Dict, List, Optional, Tuple

class SpotifyPlaylistCreator:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope="playlist-modify-public playlist-modify-private"
        ))

    # Tries to match rows to tracks on spotify using values from 'song' and 'artist' columns
    def search_track(self, artist: str, song: str) -> Optional[Dict]:
        query = f"track:{song} artist:{artist}"
        try:
            results = self.sp.search(q=query, type="track", limit=3)
            
            if not results["tracks"]["items"]:
                print(f"No results found for: {artist} - {song}")
                return None
                
            track = results["tracks"]["items"][0]
            
            track_name_lower = track["name"].lower()
            artist_name_lower = track["artists"][0]["name"].lower()
            search_song_lower = song.lower()
            search_artist_lower = artist.lower()
            
            if (search_song_lower not in track_name_lower and 
                track_name_lower not in search_song_lower):
                print(f"Warning: Potential bad match for {artist} - {song}")
                print(f"Spotify found: {track['artists'][0]['name']} - {track['name']}")
                return None
                
            return track
            
        except Exception as e:
            print(f"Error searching for {artist} - {song}: {str(e)}")
            return None
            
    def create_playlist(self, name: str, description: str) -> Optional[str]:
        try:
            user_id = self.sp.me()["id"]
            playlist = self.sp.user_playlist_create(
                user_id, 
                name,
                public=False,
                description=description
            )
            return playlist["id"]
        except Exception as e:
            print(f"Error creating playlist: {str(e)}")
            return None
            
    def add_tracks_to_playlist(self, playlist_id: str, track_ids: List[str]) -> None:
        try:
            # Adds tracks to the playlist in batches of 100 (Spotify API limit)
            for i in range(0, len(track_ids), 100):
                batch = track_ids[i:i + 100]
                self.sp.playlist_add_items(playlist_id, batch)
                time.sleep(1)  # small delay to avoid rate limiting
        except Exception as e:
            print(f"Error adding tracks to playlist: {str(e)}")

def main():
    # replace with path (or url) of csv file
    df = pd.read_csv("path/to/your/csv/file.csv")
    
    # replace CLIENT_ID, CLIENT_SECRET, REDITECT_URI with credentials from Spotify Developer Dashboard
    client_id = "CLIENT_ID"
    client_secret = "CLIENT_SECRET"
    redirect_uri = "REDIRECT_URI"
    
    spotify = SpotifyPlaylistCreator(client_id, client_secret, redirect_uri)
    
    # replace PLAYLIST_NAME and PLAYLIST_DESCRIPTION with desired values
    playlist_name = "PLAYLIST_NAME"
    playlist_description = "PLAYLIST_DESCRIPTION"
    playlist_id = spotify.create_playlist(playlist_name, playlist_description)
    
    if not playlist_id:
        print("Failed to create playlist")
        return
        
    track_ids = []
    matches = []
    no_matches = []
    
    for _, row in df.iterrows():
        track = spotify.search_track(row["artist"], row["song"])
        if track:
            track_ids.append(track["id"])
            matches.append((row["artist"], row["song"]))
        else:
            no_matches.append((row["artist"], row["song"]))
            
        time.sleep(1)
    
    if track_ids:
        spotify.add_tracks_to_playlist(playlist_id, track_ids)

    print("\nSummary:")
    print(f"Total tracks processed: {len(df)}")
    print(f"Matches found: {len(matches)}")
    print(f"No matches found: {len(no_matches)}")
    
    if matches:
        print("\nMatched tracks:")
        for artist, song in matches:
            print(f"✓ {artist} - {song}")
            
    if no_matches:
        print("\nNo matches found for:")
        for artist, song in no_matches:
            print(f"✗ {artist} - {song}")

if __name__ == "__main__":
    main()
