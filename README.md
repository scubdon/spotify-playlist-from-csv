# new spotify playlist from csv

Attempts to match rows of a csv file to tracks on Spotify and add matches to a new playlist. 


- Requires spotipy, pandas
	
- Assumes csv file contains 'song' and 'artist' columns.

- Requires credentials from [spotify developer dashboard](https://developer.spotify.com/dashboard)
    - obtain by creating new application with:
        - title/description of your choice
        - Web API enabled
        - redirect URI (can be something like `https://localhost:8888/callback`)
    - Use in place of CLIENT_ID, CLIENT_SECRET, REDIRECT_URI where noted in script

 - also need to update with path/url of csv file to use and desired playlist name/description 
