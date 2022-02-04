from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import spotipy
from pprint import pprint
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

load_dotenv()

date = input("Which year do you want to travel to?\n Type the date in this format YYYY-MM-DD")

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")


response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

song_names = [title.text.strip("\n") for title in soup.select(selector="#title-of-a-story.a-no-trucate")]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
# print(user_id)

song_uris = []
year = date.split("-")[0]
for song in song_names:
    try:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        pprint(result)
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except :
        pprint(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user_id,name=f"{date} Billboard",public=False)
sp.playlist_add_items(playlist["id"],song_uris)

