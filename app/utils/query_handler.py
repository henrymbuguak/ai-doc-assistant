import requests
from dotenv import load_dotenv
import os

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def explain_code(code_snippet, query):
    """
    Use DeepSeek LLM to explain code based on a natural language query.
    """
    prompt = f"""
    The user has provided the following Python code:
    {code_snippet}

    They are asking: "{query}"

    Provide a clear and concise explanation of what the code does, focusing on the user's query.
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7
    }
    response = requests.post(
        "https://api.deepseek.com/beta/completions",
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        raise Exception(f"Failed to generate explanation: {response.status_code}")