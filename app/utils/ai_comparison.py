import os
from openai import OpenAI
from anthropic import Anthropic

def compare_ai_tools(code):
    """
    Compare DeepSeek with OpenAI GPT and Claude for generating documentation.
    Handles errors gracefully and returns meaningful error messages.
    """
    results = {
        "deepseek": None,
        "openai_gpt": None,
        "claude": None,
        "errors": {}
    }

    # Generate documentation with DeepSeek
    try:
        from .docstring_generator import generate_markdown_docs
        results["deepseek"] = generate_markdown_docs(code)
    except Exception as e:
        results["errors"]["deepseek"] = f"DeepSeek Error: {str(e)}"

    # Generate documentation with OpenAI GPT
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        gpt_response = client.completions.create(
            model="gpt-3.5-turbo",
            prompt=f"Generate documentation for the following Python code:\n{code}"
        )
        results["openai_gpt"] = gpt_response.choices[0].text.strip()
    except Exception as e:
        results["errors"]["openai_gpt"] = f"OpenAI GPT Error: {str(e)}"

    # Generate documentation with Claude
    try:
        client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        claude_response = client.completions.create(
            model="claude-2",
            prompt=f"Generate documentation for the following Python code:\n{code}"
        )
        results["claude"] = claude_response.choices[0].text.strip()
    except Exception as e:
        results["errors"]["claude"] = f"Claude Error: {str(e)}"

    return results