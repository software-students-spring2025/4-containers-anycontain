from flask import Blueprint, request, jsonify
from app.fake_model import analyze_image

routes = Blueprint('routes', __name__)

@routes.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_bytes = file.read()
    result = analyze_image(file_bytes)

    return jsonify(result)