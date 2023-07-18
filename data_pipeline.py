from spotify_crawler import SpotifyCrawler
from data_cleaner import DataCleaner
from generate_ratings import GenerateRatings

import pandas as pd

# Accessing data from Spotify
client_id = "afbaa118b8cb4ff8959ddf7d5f2cfe73"
client_secret = "bfe2d633e86442ddacde8b4c412c879e"

crawler = SpotifyCrawler(client_id, client_secret)

playlist_urls = [
        'https://open.spotify.com/playlist/37i9dQZF1DWXT8uSSn6PRy',
        'https://open.spotify.com/playlist/37i9dQZF1DWVA1Gq4XHa6U',
        # Add more playlist URLs here
    ]

crawler.crawl(playlist_urls)


# Data cleaning
cleaner = DataCleaner('./raw_data/all_tracks.json', './clean_data/songs.csv')
cleaned_data = cleaner.clean_data()
cleaner.save_to_csv(cleaned_data)

songs_data = pd.read_csv("./clean_data/songs.csv")

song_ids = songs_data.drop_duplicates().index


# generate user-rating dataset 
num_users = 50
song_ids = song_ids
min_rating = 1
max_rating = 5
total_ratings = 300

generator = GenerateRatings(num_users, song_ids, min_rating, max_rating, total_ratings, "./clean_data/user_ratings.csv")
generator.generate_and_save_ratings()