"""Module defining Flask routes for handling image upload and detection."""

import sys
import os
import tempfile

# Add project root to sys.path to enable importing machine_learning_client
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from flask import Blueprint, request, jsonify
from machine_learning_client.database import store_image, update_classification
from machine_learning_client.detector import AnimalDetector

routes = Blueprint("routes", __name__)

def _validate_upload_file(file_obj):
    """
    Validate the uploaded file.

    Args:
        file_obj: The uploaded file object.

    Returns:
        bool: True if the file exists and has a filename, False otherwise.
    """
    if not file_obj or file_obj.filename == "":
        return False
    return True

@routes.route("/upload", methods=["POST"])
def upload_image():
    """
    Handle image upload, store the image, run detection, update classification,
    and return the results as JSON.

    Returns:
        A JSON response with the detection result, or an error message.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if not _validate_upload_file(file):
        return jsonify({"error": "No selected file"}), 400

    file_bytes = file.read()

    # Save the file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    # Store the image in the database
    inserted_id = store_image(
        file_bytes,
        animal_or_not=0,
        image_type="",
        text_description="Raw image",
        env_file="x.env",
    )

    # Create an instance of the detector and run detection
    detector = AnimalDetector()
    try:
        result = detector.detect(tmp_path)
    except Exception as e:  # pylint: disable=broad-exception-caught
        return jsonify({"error": f"detection failed: {str(e)}"}), 500

    # Update classification result in the database
    update_classification(
        inserted_id,
        animal_or_not=result["animal_or_not"],
        image_type=result["type"],
        text_description=result["text_description"],
        env_file="x.env",
    )

    return jsonify({
        "id": str(inserted_id),
        "animal_or_not": result["animal_or_not"],
        "type": result["type"],
        "text_description": result["text_description"]
    })
