import io
import sys
import pytest
from main import main


def dummy_store_image(binary_data, animal_or_not=0, image_type="", text_description="", env_file="x.env"):
    return "dummy_id"


def dummy_update_classification(document_id, animal_or_not, image_type, text_description, env_file="x.env"):
    return 1


@pytest.fixture(autouse=True)
def patch_database(monkeypatch):

    monkeypatch.setattr("main.store_image", dummy_store_image)
    monkeypatch.setattr("main.update_classification", dummy_update_classification)


def test_main_no_image(monkeypatch, tmp_path):
   
    monkeypatch.chdir(tmp_path)
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, "stdout", captured_output)
    
    main()
    output = captured_output.getvalue()
    assert "Sample image" in output