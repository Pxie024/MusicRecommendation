import requests
import json


class SpotifyCrawler:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

    def extract_playlist_ids(self, playlist_urls):
        playlist_ids = []
        for url in playlist_urls:
            playlist_id = url.split('/playlist/')[1]
            playlist_ids.append(playlist_id)
        return playlist_ids

    def extract_track_ids(self, track_urls):
        track_ids = []
        for url in track_urls:
            track_id = url.split('/tracks/')[1]
            track_ids.append(track_id)
        return track_ids

    def generate_playlist_api_requests(self, playlist_urls):
        base_url = 'https://api.spotify.com/v1/playlists'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }
        api_requests = []
        playlist_ids = self.extract_playlist_ids(playlist_urls)
        for playlist_id in playlist_ids:
            url = f'{base_url}/{playlist_id}/tracks'
            api_requests.append((url, headers))
        return api_requests

    def generate_track_api_requests(self, track_urls):
        base_url = 'https://api.spotify.com/v1/tracks'
        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }
        api_requests = []
        track_ids = self.extract_track_ids(track_urls)
        for track_id in track_ids:
            url = f'{base_url}/{track_id}'
            api_requests.append((url, headers))
        return api_requests

    def fetch_track_data(self, playlist_urls):
        all_track_data = []
        all_track_urls = []
        playlist_api_requests = self.generate_playlist_api_requests(playlist_urls)
        for url, headers in playlist_api_requests:
            response = requests.get(url, headers=headers)
            data = response.json()
            for track in data["items"]:
                all_track_urls.append(track["track"]["href"])
        
        track_api_requests = self.generate_track_api_requests(all_track_urls)
        for url, headers in track_api_requests:
            response = requests.get(url, headers=headers)
            data = response.json()
            all_track_data.append(data)
    
        # Save all track data into a single JSON file
        with open('./raw_data/all_tracks.json', 'w') as file:
            json.dump(all_track_data, file, indent=2)

    def get_access_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        response = requests.post(token_url, data=payload)
        access_token = response.json().get('access_token')
        return access_token

    def crawl(self, playlist_urls):
        self.fetch_track_data(playlist_urls)