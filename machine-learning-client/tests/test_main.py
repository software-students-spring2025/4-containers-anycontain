"""
Module for testing the main function.
"""

import io
import sys
import pytest  # pylint: disable=import-error
import main  # pylint: disable=import-error


def dummy_store_image(_binary_data, animal_or_not=0, image_type="",
                      text_description="", env_file="x.env"):
    """
    Dummy store_image function for testing.
    """
    _ = (animal_or_not, image_type, text_description, env_file)
    return "dummy_id"


def dummy_update_classification(document_id, animal_or_not, image_type,
                                text_description, env_file="x.env"):
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


def test_main_no_image(monkeypatch, tmp_path):
    """
    Test that main() behaves correctly when the sample image is missing.
    """
    monkeypatch.chdir(tmp_path)
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured_output)
    main.main()
    output = captured_output.getvalue()
    # The output should indicate that the sample image was not found.
    assert "Sample image" in output
    