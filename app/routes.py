from flask import Blueprint, jsonify, request
from .utils.docstring_generator import generate_docstring
from app.utils.github_api import fetch_repo_contents, filter_python_files, download_file_contents
from app.utils.code_parser import extract_functions_and_classes, extract_function_signature, extract_class_metadata


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return "Welcome to the AI-Powered Documentation Assistant!"

@main_bp.route('/generate-docstring', methods=['POST'])

def generate_docstring_route():
    code = request.json.get('code')
    if not code:
        return jsonify({"error": "No code provided"}), 400

    try:
        docstring = generate_docstring(code)
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
