import io
import sys
import pytest
from machine_learning_client import main


def dummy_store_image(
    _binary_data, animal_or_not=0, image_type="", text_description="", env_file="x.env"
):
    return "dummy_id"


def dummy_update_classification(
    document_id, animal_or_not, image_type, text_description, env_file="x.env"
):
    return 1


@pytest.fixture(autouse=True)
def patch_database(monkeypatch):
    monkeypatch.setattr(main, "store_image", dummy_store_image)
    monkeypatch.setattr(main, "update_classification", dummy_update_classification)


@pytest.fixture
def dummy_detector(monkeypatch):
    class DummyDetector:
        def __init__(self, use_openai=False):
            self.use_openai = use_openai

        def detect(self, image_path):
            return {
                "animal_or_not": 1,
                "type": "TestAnimal",
                "text_description": "Detected test animal.",
            }

    monkeypatch.setattr(main, "AnimalDetector", DummyDetector)


# def test_main_with_local_model(monkeypatch, tmp_path, capsys, dummy_detector):
#     monkeypatch.chdir(tmp_path)
#     test_image = tmp_path / "test.png"
#     test_image.write_bytes(b"dummy image content")

#     monkeypatch.setattr(sys, "argv", ["main.py", str(test_image)])

#     main.main()

#     captured = capsys.readouterr().out

#     assert "Stored image with id: dummy_id" in captured
#     assert "Local model detection result:" in captured
#     assert "Updated 1 document(s)" in captured


def test_main_with_openai(monkeypatch, tmp_path, capsys, dummy_detector):
    monkeypatch.chdir(tmp_path)
    test_image = tmp_path / "test.png"
    test_image.write_bytes(b"dummy image content")

    monkeypatch.setattr(sys, "argv", ["main.py", str(test_image), "--openai"])

    main.main()

    captured = capsys.readouterr().out

    assert "Stored image with id: dummy_id" in captured
    assert "OpenAI GPT-4o detection result:" in captured
    assert "Updated 1 document(s)" in captured
