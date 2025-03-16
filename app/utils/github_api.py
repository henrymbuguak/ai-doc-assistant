import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

def fetch_repo_contents(owner, repo, path=""):
    """
    Fetch the contents of a GitHub repository recursively.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        all_contents = []
        for item in contents:
            if item["type"] == "dir":
                # Recursively fetch contents of the directory
                all_contents.extend(fetch_repo_contents(owner, repo, item["path"]))
            else:
                all_contents.append(item)
        return all_contents
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
        
def fetch_and_process_repo(owner, repo):
    """
    Fetch and process all Python files in a repository.
    """
    print(f"Fetching repository contents for {owner}/{repo}...")
    contents = fetch_repo_contents(owner, repo)
    python_files = [file for file in contents if file["name"].endswith(".py")]
    all_code = ""
    for file in python_files:
        try:
            print(f"Processing file: {file['path']}")
            code = download_file_contents(file["download_url"])
            print(f"Code from {file['path']}:\n{code}\n")  # Debug: Print the fetched code
            all_code += f"# File: {file['path']}\n\n{code}\n\n"
        except Exception as e:
            print(f"Failed to process {file['path']}: {str(e)}")
    print("Repository processing complete.")
    return all_code