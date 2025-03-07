import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def generate_docstring(code_snippet, context=None):
    """
    Generate a docstring for a given code snippet using DeepSeek.
    """
    prompt = f"""
    Generate a docstring for the following Python code. Follow PEP-257 standards and include:
    - A one-line summary.
    - A detailed description (if necessary).
    - Args (for functions).
    - Returns (for functions).
    - Raises (if applicable).

    Code:
    {code_snippet}

    Context:
    {context if context else "No additional context provided."}
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # Specify the model
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
        # Print the response details for debugging
        print(f"API Response: {response.status_code}, {response.text}")
        raise Exception(f"Failed to generate docstring: {response.status_code}")


def improve_docstring(existing_docstring, context=None):
    """
    Improve an existing docstring using DeepSeek.
    """
    prompt = f"""
    Improve the following docstring for clarity, readability, and completeness. Convert passive voice to active voice where applicable.

    Docstring:
    {existing_docstring}

    Context:
    {context if context else "No additional context provided."}
    """

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",  # Specify the model
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7
    }
    response = requests.post(
        "https://api.deepseek.com/beta/completions",  # Use the beta endpoint
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        # Print the response details for debugging
        print(f"API Response: {response.status_code}, {response.text}")
        raise Exception(f"Failed to improve docstring: {response.status_code}")    


