import os
import requests
from .code_parser import extract_functions_and_classes, extract_function_signature, extract_class_metadata
from dotenv import load_dotenv
from .query_handler import explain_code

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

def generate_markdown_docs(code):
    """
    Generate enhanced Markdown documentation from Python code using AI.
    """
    functions, classes = extract_functions_and_classes(code)
    docs = "# API Documentation\n\n"

    # Add function documentation
    docs += "## Functions\n\n"
    for func in functions:
        signature = extract_function_signature(func)
        docs += f"### `{signature['name']}`\n"
        docs += f"**Arguments:** `{', '.join(signature['args'])}`\n\n"
        docs += f"**Returns:** `{signature['returns']}`\n\n"

        # Generate AI explanation for the function
        explanation = explain_code(func, f"What does the function `{signature['name']}` do?")
        docs += f"**Explanation:** {explanation}\n\n"

        # Generate AI example usage for the function
        example = explain_code(func, f"Provide an example usage for the function `{signature['name']}`.")
        docs += f"**Example Usage:**\n```python\n{example}\n```\n\n"

    # Add class documentation
    docs += "## Classes\n\n"
    for cls in classes:
        metadata = extract_class_metadata(cls)
        docs += f"### `{metadata['name']}`\n"
        docs += f"**Methods:** `{', '.join(metadata['methods'])}`\n\n"
        docs += f"**Docstring:** {metadata['docstring']}\n\n"

        # Generate AI explanation for the class
        explanation = explain_code(cls, f"What does the class `{metadata['name']}` do?")
        docs += f"**Explanation:** {explanation}\n\n"

        # Generate AI example usage for the class
        example = explain_code(cls, f"Provide an example usage for the class `{metadata['name']}`.")
        docs += f"**Example Usage:**\n```python\n{example}\n```\n\n"

    return docs

def generate_html_docs(markdown_docs):
    """
    Convert Markdown documentation to HTML.
    """
    import markdown
    return markdown.markdown(markdown_docs)

def save_docs(docs, filename):
    """
    Save documentation to a file in the /docs folder.
    If the /docs folder doesn't exist, create it.
    """
    # Ensure the /docs folder exists
    os.makedirs("docs", exist_ok=True)
    # Save the file in the /docs folder
    with open(f"docs/{filename}", "w") as f:
        f.write(docs)

def push_to_github(docs, repo_name, branch="gh-pages"):
    """
    Push documentation to GitHub Pages.
    """
    import subprocess
    # Save docs to a temporary file in the /docs folder
    save_docs(docs, "index.html")
    # Push the /docs folder to GitHub Pages
    subprocess.run(["git", "add", "docs/"])
    subprocess.run(["git", "commit", "-m", "Update documentation"])
    subprocess.run(["git", "push", "origin", branch])


def detect_outdated_docs(code, docs):
    """
    Detect outdated documentation by comparing code and docs.
    """
    current_docs = generate_markdown_docs(code)
    if current_docs != docs:
        return "Documentation is outdated. Please regenerate."
    return "Documentation is up-to-date."

def tag_documentation_version(version):
    """
    Tag the current documentation with a version number.
    """
    import subprocess
    subprocess.run(["git", "tag", f"v{version}"])
    subprocess.run(["git", "push", "origin", f"v{version}"])
