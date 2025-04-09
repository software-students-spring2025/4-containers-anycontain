import io
import sys
import pytest
from machine_learning_client import main


def dummy_store_image(
    _binary_data, animal_or_not=0, image_type="", text_description="", env_file="x.env"
):
    """
    Dummy store_image function for testing.
    """
    _ = (animal_or_not, image_type, text_description, env_file)
    return "dummy_id"


def dummy_update_classification(
    document_id, animal_or_not, image_type, text_description, env_file="x.env"
):
    """
    Dummy update_classification function for testing.
    """
    _ = (document_id, animal_or_not, image_type, text_description, env_file)
    return 1


@pytest.fixture(autouse=True)
def patch_database(monkeypatch):
    """
    Patch the database functions in main with dummy functions.
    """
    monkeypatch.setattr(main, "store_image", dummy_store_image)
    monkeypatch.setattr(main, "update_classification", dummy_update_classification)

