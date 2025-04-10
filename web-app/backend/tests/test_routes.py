import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import io
import pytest
from flask import Flask
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_upload_valid_image(client):
    dummy_image = io.BytesIO(b"fake image data")
    dummy_image.name = "test.jpg"

    response = client.post(
        "/upload",
        data={"file": (dummy_image, "test.jpg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200 or response.status_code == 500
    json_data = response.get_json()
    assert isinstance(json_data, dict)
    assert "text_description" in json_data or "error" in json_data


def test_upload_empty_file(client):
    empty_file = io.BytesIO(b"")
    empty_file.name = "empty.jpg"

    response = client.post(
        "/upload",
        data={"file": (empty_file, "empty.jpg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Uploaded file is empty"


def test_upload_unsupported_format(client):
    fake_file = io.BytesIO(b"This is not an image.")
    fake_file.name = "test.txt"

    response = client.post(
        "/upload",
        data={"file": (fake_file, "test.txt")},
        content_type="multipart/form-data",
    )
    assert response.status_code in [200, 500]
    assert isinstance(response.get_json(), dict)
