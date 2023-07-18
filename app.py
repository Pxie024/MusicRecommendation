from flask import Flask, render_template, request
from recommendation_system import CollaborativeFilteringRS

app = Flask(__name__)

# Initialize the CollaborativeFilteringRS instance
songs_dataset_file = './clean_data/songs.csv'
user_ratings_file = './clean_data/user_ratings.csv'
rs = CollaborativeFilteringRS(songs_dataset_file, user_ratings_file)

# Load the datasets and train the model
songs_df, data = rs.load_datasets()
songs_df['itemID'] = songs_df.index
model = rs.train_model(data)

@app.route('/')
def index():
    num_songs_to_rate = 5
    sampled_songs = songs_df.sample(num_songs_to_rate)
    return render_template('rate_songs.html', songs=sampled_songs.to_dict(orient='records'))

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    user_ratings = []
    for idx in range(5):
        song_id = int(request.form.get(f'song_{idx}'))
        rating = int(request.form.get(f'rating_{idx}'))
        user_ratings.append({'itemID': song_id, 'rating': rating})

    num_recommendations = 3
    recommendations = rs.get_recommendations(model, user_ratings, num_recommendations)
    recommended_songs = songs_df[songs_df['itemID'].isin(recommendations)]
    return render_template('recommendations.html', songs=recommended_songs.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)