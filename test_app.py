import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Movie Rating Prediction API is running!" in response.data

def test_predict_valid(client):
    response = client.post('/predict', json={
        'user_id': 1,
        'movie_id': 1
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data

def test_predict_missing_data(client):
    response = client.post('/predict', json={
        'user_id': 1
        # 'movie_id' is missing
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_predict_invalid_data(client):
    response = client.post('/predict', json={
        'user_id': 'invalid',
        'movie_id': 'invalid'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data