import random
import csv

class GenerateRatings:
    def __init__(self, num_users, song_ids, min_rating, max_rating, total_ratings, filename):
        self.num_users = num_users
        self.songs = song_ids
        self.min_rating = min_rating
        self.max_rating = max_rating
        self.total_ratings = total_ratings
        self.filename = filename

    def generate_dataset(self):
        dataset = []
        users = list(range(1, self.num_users + 1))
        
        for _ in range(self.total_ratings):
            user = random.choice(users)
            song = random.choice(self.songs)
            rating = random.randint(self.min_rating, self.max_rating)
            dataset.append([user, song, rating])

        return dataset

    def save_to_csv(self, dataset):
        with open(self.filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['userID', 'itemID', 'rating'])
            csvwriter.writerows(dataset)

    def generate_and_save_ratings(self):
        dataset = self.generate_dataset()
        self.save_to_csv(dataset)

