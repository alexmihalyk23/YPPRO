import pytest
import io
from app import app
from bs4 import BeautifulSoup

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    soup = BeautifulSoup(rv.data, 'html.parser')
    assert soup.find(class_='progress-bar-label') is not None


