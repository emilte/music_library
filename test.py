import spotipy
import spotipy.util as util
import json

#results = spotify.search(q='artist:Lena', type='artist')
#prin(results)

# https://open.spotify.com/user/emiltelstad?si=h64-e6V-SzWjyUwOmUTuEA
def trace(x):
    print(json.dumps(x, indent=4, sort_keys=True))


client_id = '6b34a08ef909414181faaedf68ec4304'
client_secret = 'c7935f0ff3f140c2a87df8117b82241b'
username = 'emiltelstad'
scope = 'user-library-read playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private'
redirect_uri = 'http://google.com/'

token = util.prompt_for_user_token(username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

spotify = spotipy.Spotify(auth=token)

playlist = spotify.user_playlist_create(user=username, name="TESTING")

spotify.user_playlist_replace_tracks(user=username, playlist_id=playlist['id'],
    tracks=[
        '4c6vZqYHFur11FbWATIJ9P',
    ]
)
