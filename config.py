import os

class Config:
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
