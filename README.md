# Music Recommendation Based on User Ratings

## Overview
This project builds a simple music recommendation system using collaborative filtering. The music metadata being used is real-world data from Spotify, fetched by a web crawler. Due to the fact that I do not have access to real users data, I deceided to generate a dummy data set using complete random numbers. The recommendation system is machine learning based, using the singular value decomposition ([SVD](https://en.wikipedia.org/wiki/Singular_value_decomposition)) algorithm, which is very popular for collaborative filtering. The model is implemented in Python using the [Surprise](https://surpriselib.com/) library built by Scikit-learn. This module is specifically designed for recommender systems, and has a lot of the nice features of other `sklearn` modules. 

The final product works as follows: it will ask a new user to rate a number of (default 5) randomly selected songs on a scale of 1 to 5, with 1 being dislike and 5 being like. It will then recommend some (default 3) song tracks the user is mostly likely to enjoy, based on the predicted result of user rating for all other songs. I have built a very simple user interface: 

![rate songs](https://github.com/Pxie024/MusicRecommendation/assets/59588558/b56ca080-9178-4e78-8813-8111d17179da)

After hitting the **Submit** button, the system will return some recommended music to the user. 

![recommended](https://github.com/Pxie024/MusicRecommendation/assets/59588558/c12efea7-9706-426f-b242-05771f38c858)


## Files
Some important files and folders in this project: 
* `spotify_crawler.py`: a web crawler to access music metadata from Spotify, saves the results in `raw_data` directory as a `.json` file.
* `data_cleaner.py`: cleans the raw data to retain only the useful information, saves the results in `clean_data` as a `.csv` file.
* `generate_ratings.py`: a filed used to generate dummy user ratings, saves the results in `clean_data` as a `.csv` file. The final output is a table of three columns: "`userID`", "`itemIS`", and "`rating`".
* `data_pipeline.py`: a pipeline to automate the above processes. Run this file using `python data_pipeline.py` to streamline the data gathering, cleaning and generating process.
* `recommendation_system.py`: a file that contains the logic of the system, it is the brain of the whole project. Can be run separately after the data pipeline by `python recommendation_system.py`.
* `app.py`: deploys the logic into a Flask app. Contains two RESTapis, which corresponds to the two stages of the interface (asking ratings, results).
* `templates`: a directory that contains `.html` templates of the app.


## Instructions
If you intent to run this project on your local computer, please follow these steps: 
1. clone this repo onto your local directory using `git clone`.
2. in the terminal, run `python data_pipeline.py` to generate necessary data.
3. you then have the option to run the recommendation system in the terminal or as a web application. To run the system in terminal, run `python recommendation_system.py`, then start input your ratings as integers.
   To run this as a web application, run `python app.py`, then open a browser (prefererably Chrome) and enter the URL that pops up in your terminal (typically something like http://127.0.0.1:5000).


Please note: though it has its usecases in the real world, this project is by no mean at industry standard at this point. The purpose of this project is for me to demostrate my software development skills, as well as figuring out how my skillset can potentially impact the music industry. To make the system more reliable, more data is needed, as well as access to real-world user data. Also, unit testing needs to be added to all aspects of the project. 
