from flask import Blueprint, jsonify, request
from .utils.docstring_generator import generate_docstring

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
