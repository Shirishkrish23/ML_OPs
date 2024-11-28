import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import pickle

# Load data
ratings = pd.read_csv('u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
item_cols = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown',
             'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama',
             'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
             'War', 'Western']
movies = pd.read_csv('u.item', sep='|', names=item_cols, encoding='ISO-8859-1')
data = pd.merge(ratings, movies, on='movie_id').fillna(0)

# Encode and normalize
le_title = LabelEncoder()
data['movie_title_encoded'] = le_title.fit_transform(data['movie_title'])
scaler = MinMaxScaler()
data[['user_id', 'movie_title_encoded']] = scaler.fit_transform(data[['user_id', 'movie_title_encoded']])

features = ['user_id', 'movie_title_encoded'] + item_cols[5:]
target = 'rating'

X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2, random_state=42)

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [20, None],
    'min_samples_split': [10]
}

# Train the model
model = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3)
model.fit(X_train, y_train)

best_model = model.best_estimator_
y_pred = best_model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE: {rmse}")

# Set the RMSE threshold
max_rmse = 1.2  # Define your acceptable RMSE threshold

if rmse <= max_rmse:
    # Save LabelEncoder and model
    with open('title_encoder.pkl', 'wb') as f:
        pickle.dump(le_title, f)
    with open('optimized_movie_rating_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    print(f"Model retrained and saved with RMSE: {rmse}")
else:
    print(f"Model RMSE {rmse} exceeded threshold {max_rmse}. Model not updated.")