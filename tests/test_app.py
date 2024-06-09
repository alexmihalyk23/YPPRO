import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Hello, World!" in rv.data

def test_upload_file(client):
    data = {
        'file': (io.BytesIO(b'my file contents'), 'test.zip')
    }
    rv = client.post('/', data=data)
    assert rv.status_code == 200
    assert b"File saved" in rv.data

def test_progress(client):
    rv = client.get('/progress')
    assert rv.status_code == 200

def test_download_file(client):
    rv = client.get('/download/test.zip')
    assert rv.status_code == 200
