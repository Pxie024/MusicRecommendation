from surprise import Dataset, Reader
from surprise import SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
import pandas as pd

class CollaborativeFilteringRS:
    def __init__(self, songs_dataset_file, user_ratings_file):
        self.songs_dataset_file = songs_dataset_file
        self.user_ratings_file = user_ratings_file

    def load_datasets(self):
        # Load songs dataset
        songs_df = pd.read_csv(self.songs_dataset_file)
        songs_df['itemID'] = songs_df.index

        # Load user ratings dataset
        reader = Reader(rating_scale=(1, 5))
        user_ratings_df = pd.read_csv(self.user_ratings_file)
        data = Dataset.load_from_df(user_ratings_df[['userID', 'itemID', 'rating']], reader)

        return songs_df, data

    def train_model(self, data):
        # Split the dataset into training and testing sets
        trainset, testset = train_test_split(data, test_size=0.2, random_state=420)

        # Use the SVD algorithm for collaborative filtering
        model = SVD()

        # Train the model on the training set
        model.fit(trainset)

        # Evaluate the model on the test set
        predictions = model.test(testset)

        # Compute RMSE (Root Mean Squared Error) to evaluate the model's performance
        rmse = accuracy.rmse(predictions)
        print(f"RMSE: {rmse}")

        return model

    def get_recommendations(self, model, user_ratings, num_recommendations=10):
        # Get all song IDs
        songs_df, _ = self.load_datasets()
        all_song_ids = songs_df['itemID'].tolist()

        # Get the list of song IDs rated by the user
        rated_song_ids = [rating['itemID'] for rating in user_ratings]

        # Remove the rated song IDs from the list of all song IDs
        remaining_song_ids = [song_id for song_id in all_song_ids if song_id not in rated_song_ids]

        # Predict ratings for the remaining song IDs
        predictions = [model.predict(0, song_id) for song_id in remaining_song_ids]

        # Sort predictions based on predicted ratings in descending order
        predictions.sort(key=lambda x: x.est, reverse=True)

        # Get the top N recommendations
        top_n_recommendations = [prediction.iid for prediction in predictions[:num_recommendations]]

        return top_n_recommendations

def main():
    # Define the paths to the datasets
    songs_dataset_file = 'songs.csv'
    user_ratings_file = 'user_ratings.csv'

    # Create an instance of the CollaborativeFilteringRS class
    rs = CollaborativeFilteringRS(songs_dataset_file, user_ratings_file)

    # Load the datasets
    songs_df, data = rs.load_datasets()
    songs_df['itemID'] = songs_df.index

    # Train the collaborative filtering model
    model = rs.train_model(data)

    # Randomly choose a few songs to present to the user for rating
    num_songs_to_rate = 5
    sampled_songs = songs_df.sample(num_songs_to_rate)
    user_ratings = []
    print("Please rate the following songs (1 to 5, or enter '0' if not familiar):")
    for idx, song_info in sampled_songs.iterrows():
        song_id = song_info['itemID']
        song_name = song_info['Track Name']
        artist_name = song_info['Artists']
        rating = int(input(f"{song_name} - {artist_name} (Enter your rating from 1 to 5): "))
        user_ratings.append({'itemID': song_id, 'rating': rating})

    # Get recommendations for the new user
    num_recommendations = 3
    recommendations = rs.get_recommendations(model, user_ratings, num_recommendations)
    print(f"Top {num_recommendations} Recommendations for You:")
    for i, song_id in enumerate(recommendations, start=1):
        song_info = songs_df[songs_df['itemID'] == song_id].iloc[0]
        song_name = song_info['Track Name']
        artist_name = song_info['Artists']
        print(f"{i}. {song_name} - {artist_name}")

if __name__ == "__main__":
    main()