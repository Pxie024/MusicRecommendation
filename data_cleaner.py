import json
import csv

class DataCleaner:
    def __init__(self, json_file, csv_file):
        self.json_file = json_file
        self.csv_file = csv_file
    
    def clean_data(self):
        with open(self.json_file) as json_file:
            json_data = json.load(json_file)
        
        cleaned_data = []
        available_markets_set = set()  # To collect unique available markets
        
        for track in json_data:
            artists = ', '.join([artist['name'] for artist in track['artists']])
            album_name = track['album']['name']
            album_type = track['album']['album_type']
            track_name = track['name']
            track_url = track['external_urls']['spotify']
            popularity = track['popularity']
            is_explicit = track['explicit']
            duration_ms = track['duration_ms']
            album_image_url = track['album']['images'][0]['url']
            release_date = track['album']['release_date']
            is_local = track['is_local']
            available_markets = track['available_markets']
            
            cleaned_data.append({
                'Artists': artists,
                'Album Name': album_name,
                'Album Type': album_type,
                'Track Name': track_name,
                'Track URL': track_url,
                'Popularity': popularity,
                'Explicit': is_explicit,
                'Duration (ms)': duration_ms,
                'Album Image URL': album_image_url,
                'Release Date': release_date,
                'Local': is_local,
                'Number of Markets': len(available_markets),
                'Available Markets': available_markets
            })
            
            available_markets_set.update(available_markets)
        
        # Create one-hot encoded columns for available markets
        available_markets_list = list(available_markets_set)
        for market in available_markets_list:
            for data in cleaned_data:
                data[market] = 1 if market in data['Available Markets'] else 0
        
        return cleaned_data
    
    def save_to_csv(self, data):
        keys = data[0].keys()
        
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)