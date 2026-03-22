from dotenv import load_dotenv
import requests
import json
import os


load_dotenv(dotenv_path='./.env')

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = "MrBeast"


def get_playlist_id():

    try:
        url = 'https://youtube.googleapis.com/youtube/v3/channels'
        params = {
            'part':'contentDetails',
            'forHandle': CHANNEL_HANDLE,
            'key': API_KEY
        }

        response = requests.get(url, params=params)

        response.raise_for_status()

        data = response.json()

        # Convert json to json-formatted string
        #print(json.dumps(data, indent = 4))

        channel_items = data["items"][0]

        channel_playlistid = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(channel_playlistid)

        return channel_playlistid
    
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == "__main__":
    get_playlist_id()