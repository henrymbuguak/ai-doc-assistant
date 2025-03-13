from flask import Blueprint, jsonify, request, render_template
from .utils.docstring_generator import generate_docstring, improve_docstring, generate_markdown_docs, generate_html_docs, save_docs
from app.utils.github_api import fetch_repo_contents, filter_python_files, download_file_contents
from app.utils.code_parser import extract_functions_and_classes, extract_function_signature, extract_class_metadata
from .utils.query_handler import explain_code
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

main_bp = Blueprint('main', __name__)

# Rate limiting for API endpoints
limiter = Limiter(key_func=get_remote_address)

@main_bp.route('/')
def home():
    return render_template("index.html") 

@main_bp.route('/generate-docstring', methods=['POST'])
def generate_docstring_route():
    """
    Generate a docstring for a given code snippet.
    """
    data = request.json
    code_snippet = data.get("code")
    context = data.get("context", "")

    try:
        docstring = generate_docstring(code_snippet, context)
        return jsonify({"docstring": docstring})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main_bp.route("/fetch-repo", methods=["POST"])
def fetch_repo():
    """
    Fetch and display Python files from a GitHub repository.
    """
    data = request.json
    owner = data.get("owner")
    repo = data.get("repo")

    try:
        contents = fetch_repo_contents(owner, repo)
        python_files = filter_python_files(contents)
        return jsonify({"python_files": python_files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/parse-file", methods=["POST"])
def parse_file():
    """
    Parse a Python file and extract metadata.
    """
    data = request.json
    download_url = data.get("download_url")

    try:
        code = download_file_contents(download_url)
        functions, classes = extract_functions_and_classes(code)
        function_metadata = [extract_function_signature(func) for func in functions]
        class_metadata = [extract_class_metadata(cls) for cls in classes]
        return jsonify({
            "functions": function_metadata,
            "classes": class_metadata
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/improve-docstring", methods=["POST"])
def improve_docstring_route():
    """
    Improve an existing docstring.
    """
    data = request.json
    existing_docstring = data.get("docstring")
    context = data.get("context", "")

    try:
        improved_docstring = improve_docstring(existing_docstring, context)
        return jsonify({"improved_docstring": improved_docstring})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/explain-code", methods=["POST"])
@limiter.limit("10 per minute")
def explain_code_route():
    """
    Explain code functionality based on a natural language query.
    """
    data = request.json
    code_snippet = data.get("code")
    query = data.get("query")

    try:
        explanation = explain_code(code_snippet, query)
        return jsonify({"explanation": explanation})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/chatbot", methods=["POST"])
@limiter.limit("10 per minute")  # Rate limit to prevent abuse
def chatbot_route():
    """
    Chatbot endpoint for interactive code understanding.
    """
    data = request.json
    user_input = data.get("input")
    code_snippet = data.get("code", "")

    try:
        # Use the same explain_code utility for chatbot responses
        response = explain_code(code_snippet, user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route("/generate-docs", methods=["POST"])
def generate_docs_route():
    """
    Generate Markdown and HTML documentation from a code snippet.
    """
    data = request.json
    code_snippet = data.get("code")

    try:
        # Generate Markdown documentation
        markdown_docs = generate_markdown_docs(code_snippet)
        save_docs(markdown_docs, "docs.md")  # Save Markdown to /docs/docs.md

        # Generate HTML documentation
        html_docs = generate_html_docs(markdown_docs)
        save_docs(html_docs, "index.html")  # Save HTML to /docs/index.html

        return jsonify({
            "message": "Documentation generated successfully!",
            "markdown_docs": markdown_docs,
            "html_docs": html_docs
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500