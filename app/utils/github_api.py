import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

def fetch_repo_contents(owner, repo):
    """
    Fetch the contents of a GitHub repository.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch repository contents: {response.status_code}")

def filter_python_files(contents):
    """
    Filter out Python files from the repository contents.
    """
    return [file for file in contents if file["name"].endswith(".py")]

def download_file_contents(download_url):
    """
    Download the raw content of a file from GitHub.
    """
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    response = requests.get(download_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

def make_github_request(url):
    """
    Make a GitHub API request with rate limit handling.
    """
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 and "rate limit" in response.text:
            reset_time = int(response.headers["X-RateLimit-Reset"])
            sleep_time = max(reset_time - time.time(), 0) + 1  # Add 1 second buffer
            print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)
        else:
            raise Exception(f"Failed to make request: {response.status_code}")