import requests
import os

def generate_docstring(code):
    api_url = "https://api.deepseek.com/v1/docstring"
    headers = {"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"}
    payload = {"code": code}

    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("docstring")
    else:
        raise Exception(f"Failed to generate docstring: {response.status_code}")
