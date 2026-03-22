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
    

def get_video_ids(playlistID):

    # Create blank list
    video_ids = []

    # Create pageToken variable
    pageToken = None
  
    base_url = 'https://youtube.googleapis.com/youtube/v3/playlistItems'
    params = {
        'part': 'contentDetails',
        'maxResults': MAX_RESULTS,
        'playlistId': playlistID,
        'key': API_KEY
    }

    try:
        # when no page tokens left to append to video_id variable, break loop
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


def extract_video_data(video_ids):
    extracted_data = []


    def batch_list(video_id_lst, batch_size):
        for video_id in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[video_id: video_id + batch_size]

    

    try:
        for batch in batch_list(video_ids, MAX_RESULTS):
            video_ids_str = ','.join(batch)

            url = 'https://youtube.googleapis.com/youtube/v3/videos'
            params = {
                'part': 'contentDetails, statistics, snippet',
                'id' : video_ids_str,
                'key': API_KEY
            }

            response = requests.get(url, params=params)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'publishedAt': snippet['publishedAt'],
                    'duration': contentDetails['duration'],
                    'viewCount': statistics.get('viewCount', None),
                    'likeCount': statistics.get('likeCount', None),
                    'commentCount': statistics.get('commentCount', None)
                }  

                extracted_data.append(video_data)

        return extracted_data   


    except requests.exceptions.RequestException as e:
        raise e
if __name__ == "__main__":
    playlistID = get_playlist_id()
    video_ids = get_video_ids(playlistID)
    print(extract_video_data(video_ids))
    