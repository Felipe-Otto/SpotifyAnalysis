import json
import requests

# Obtaining Spotify API credentials from 'spotify_client.txt'
def get_client_data():
    credentials_extracted = {}
    try:
        with open('./spotify_credentials.txt') as credentials:
            for line in credentials.read().split('\n'):
                key, value = line.split('=')
                credentials_extracted[key] = value
    except Exception as e:
        print(f'An error occurred: {e}')
    return credentials_extracted

# Obtaining client token
def get_token(client_id, client_secret):
    token_url = 'https://accounts.spotify.com/api/token'
    data = {'grant_type': 'client_credentials'}
    try:
        response = requests.post(token_url, data=data, auth=(client_id, client_secret))
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            print(f'Failed to obtain the token. Status code: {response.status_code}')
    except Exception as e:
        print(f'An error occurred in the request: {e}')

# Creating API connection
def get_api_connection(token):
    headers = {'Authorization': f'Bearer {token}'}
    playlists = {'Rock': '74PRLWnKWcfK36aYLCGebz', 'Rap': '2JXzQNe5sWUxHnEwiow7HM',
                 'Mpb': '2uNtfp6YXPQMw6BMnsKvli', 'Electronic': '6bXGnyNvhHMx5ihFcOVw7z'}
    for playlist_name, playlist_id in playlists.items():
        api_url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                # Extracting playlist data
                get_playlist_data(response.json(), api_url, headers)
                print(f'\033[92m{playlist_name} playlist data successfully extracted!\033[0m')
            else:
                print(f'Failed to obtain the playlist. Status code: {response.status_code}')
        except Exception as e:
            print(f'An error occurred in the request: {e}')
            return None


# Extracting playlist data
def get_playlist_data(response, api_url, headers):
    playlist_name = response['name']
    playlist_details = filter_track_data(response, details=True)
    total_tracks = response['tracks']['total']
    limit_requisitions = 100
    tracks = []
    for offset in range(0, total_tracks, limit_requisitions):
        params = {
            "offset": offset,
            "limit": limit_requisitions
        }
        response_tracks = requests.get(f'{api_url}/tracks', headers=headers, params=params)
        if response_tracks.status_code == 200:
            tracks.extend(filter_track_data(response_tracks.json(), tracks=True))

    playlist_details['Tracks'] = tracks

    with open(f'extraction/{playlist_name}-Database.json', 'w', encoding='utf-8') as file:
        json.dump(playlist_details, file, indent=4, ensure_ascii=False)


# Filtering fields from API return
def filter_track_data(response, details=False, tracks=False):
    if details:
        playlist_details = {'Playlist Name': response['name'],
                            'Followers': response['followers']['total'],
                            'Image': response['images'][0]['url'],
                            'Total Tracks': response['tracks']['total']}
        return playlist_details
    if tracks:
        track_list = []
        for track in response['items']:
            track_details = {
                'Track Name': track['track']['name'],
                'Artist Name': track['track']['artists'][0]['name'],
                'Album Name': track['track']['album']['name'],
                'Album Release Date': track['track']['album']['release_date'],
                'Added At': track['added_at'],
                'Track Image': track['track']['album']['images'][1]['url']
            }
            track_list.append(track_details)
        return track_list
