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
    _ = (document_id, animal_or_not, image_type, text_description, env_file)
    return 1


@pytest.fixture(autouse=True)
def patch_database(monkeypatch):
    monkeypatch.setattr(main, "store_image", dummy_store_image)
    monkeypatch.setattr(main, "update_classification", dummy_update_classification)


def test_main_with_arg(monkeypatch, tmp_path, capsys):
    monkeypatch.chdir(tmp_path)
    test_image = tmp_path / "test.png"
    test_image.write_bytes(b"dummy image content")

    monkeypatch.setattr(sys, "argv", ["main.py", str(test_image)])
    monkeypatch.setattr(main, "store_image", lambda binary_data, **kwargs: "dummy_id")

    from machine_learning_client.detector import AnimalDetector

    monkeypatch.setattr(
        AnimalDetector,
        "detect",
        lambda self, image_path: {
            "animal_or_not": 1,
            "type": "TestAnimal",
            "text_description": "Detected test animal.",
        },
    )

    monkeypatch.setattr(main, "update_classification", lambda *args, **kwargs: 1)

    main.main()

    captured = capsys.readouterr().out

    assert "Stored image with id: dummy_id" in captured
    assert "Detection result:" in captured
    assert "Updated 1 document(s)" in captured
