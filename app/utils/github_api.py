import requests

def fetch_repo_code(repo_url, access_token):
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch repository: {response.status_code}")