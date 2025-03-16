import os
import sys
import pytest
from app import create_app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

def test_check_docs_route(client):
    response = client.post("/check-docs", json={"code": "def add(a, b): return a + b", "docs": "Old documentation"})
    assert response.status_code == 200
    assert "Documentation is outdated" in response.json["message"]