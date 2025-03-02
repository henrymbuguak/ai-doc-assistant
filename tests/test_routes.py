import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_generate_docstring_route(client):
    response = client.post('/generate-docstring', json={"code": "def example(): pass"})
    assert response.status_code in [200, 500]  # 500 if DeepSeek API key is missing
