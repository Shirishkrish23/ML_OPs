from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
from prometheus_flask_exporter import PrometheusMetrics  # Import PrometheusMetrics

# Load the trained model
with open('optimized_movie_rating_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Load the LabelEncoder
with open('title_encoder.pkl', 'rb') as file:
    le_title = pickle.load(file)

# Load the ratings and movies data
ratings = pd.read_csv('u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
item_cols = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown',
             'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama',
             'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
             'War', 'Western']
movies = pd.read_csv('u.item', sep='|', names=item_cols, encoding='ISO-8859-1')

# Merge the data on 'movie_id'
data = pd.merge(ratings, movies, on='movie_id')

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # Initialize Prometheus metrics

@app.route('/')
def home():
    return "Movie Rating Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from POST request
    json_data = request.get_json(force=True)

    # Extract user_id and movie_id
    user_id = json_data.get('user_id')
    movie_id = json_data.get('movie_id')

    # Handle missing data
    if user_id is None or movie_id is None:
        return jsonify({'error': 'Missing user_id or movie_id'}), 400

    # Convert user_id and movie_id to integers
    try:
        user_id = int(user_id)
        movie_id = int(movie_id)
    except ValueError:
        return jsonify({'error': 'Invalid user_id or movie_id'}), 400

    # Find the data row where both user_id and movie_id match
    user_movie_data = data[(data['user_id'] == user_id) & (data['movie_id'] == movie_id)]
    if user_movie_data.empty:
        return jsonify({'error': 'No data found for the given user_id and movie_id'}), 400

    # Since there may be multiple ratings, take the first one
    user_movie_row = user_movie_data.iloc[0]

    # Encode the movie title
    try:
        movie_title_encoded = le_title.transform([user_movie_row['movie_title']])[0]
    except ValueError:
        return jsonify({'error': 'Movie title not recognized'}), 400

    # Get the genres as a list
    genres = user_movie_row[item_cols[5:]].tolist()  # List of genre flags

    # Prepare the features
    features = [user_id, movie_title_encoded] + genres
    features = np.array(features).reshape(1, -1)

    # Make prediction
    prediction = model.predict(features)

    # Return the prediction
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)