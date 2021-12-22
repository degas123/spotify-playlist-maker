import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
Client_ID = ${{secrets.CLIENT_ID}}
Client_Secret = ${{secrets.CLIENT_SECRET}}
OAUTH_AUTHORIZE_URL= ${{secrets.OAUTH_AUTHORIZE_URL}}


date = input("Which year do you want to travel to Type the date in this format YYYY-MM-DD\n")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

responce = requests.get(URL)
top_music = responce.text
soup = BeautifulSoup(top_music, "html.parser")
song_name_spans = soup.find_all("span", class_="chart-element__information__song")
song_name = [song.getText() for song in song_name_spans]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-"[0])
for song in song_name:
    result = sp.search(q=f"track:{song}", limit=1, offset=1, type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
