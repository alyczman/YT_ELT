from dotenv import load_dotenv
import requests
import json
import os


load_dotenv(dotenv_path='./.env')

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = "MrBeast"
MAX_RESULTS = 50


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

        # print(channel_playlistid)

        return channel_playlistid
    
    except requests.exceptions.RequestException as e:
        raise e
    

#playlistID = get_playlist_id()

def get_video_ids(playlistID):

    video_ids = []

    pageToken = None
  

    base_url = 'https://youtube.googleapis.com/youtube/v3/playlistItems'
    params = {
        'part': 'contentDetails',
        'maxResults': MAX_RESULTS,
        'playlistId': playlistID,
        'key': API_KEY
    }

    try:
        # when no page tokens left, break
        while True:

            url = base_url

            if pageToken:
                #Append the page token to the url variable 
                params['pageToken'] = pageToken

            response = requests.get(url, params=params)

            response.raise_for_status()

            data = response.json()

            # use for loop to append video ids to video_id variable
            # Empty list in loop prevents crashing if key is null or not found

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e



if __name__ == "__main__":
    playlistID = get_playlist_id()
    