import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from flask import Blueprint, request, jsonify
from machine_learning_client.database import store_image, update_classification
from machine_learning_client.detector import AnimalDetector
import tempfile

routes = Blueprint("routes", __name__)


@routes.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_bytes = file.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    inserted_id = store_image(
        file_bytes,
        animal_or_not=0,
        image_type="",
        text_description="Raw image",
        env_file="x.env",
    )

    detector = AnimalDetector()
    try:
        result = detector.detect(tmp_path)
    except Exception as e:
        return jsonify({"error": f"detection failed: {str(e)}"}), 500

    update_classification(
        inserted_id,
        animal_or_not=result["animal_or_not"],
        image_type=result["type"],
        text_description=result["text_description"],
        env_file="x.env",
    )

    return jsonify(
        {
            "id": str(inserted_id),
            "animal_or_not": result["animal_or_not"],
            "type": result["type"],
            "text_description": result["text_description"],
        }
    )
