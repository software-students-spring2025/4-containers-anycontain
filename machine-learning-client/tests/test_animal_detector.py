"""
Module for testing the animal_detector module.
"""

import pytest  # pylint: disable=import-error
from animal_detector import AnimalDetector  # pylint: disable=import-error


class DummyProcessor:
    """Dummy processor to simulate model processing for tests."""

    def __init__(self):
        pass

    def __call__(self, images, return_tensors):
        """Simulate processing of images."""
        return {"dummy": "tensor"}

    def batch_decode(self, outputs, skip_special_tokens):
        """Simulate decoding of model outputs."""
        return [
            "Animal Detected: Yes. Type: Elephant. "
            "Description: Detected an elephant in the image."
        ]


class DummyModel:
    """Dummy model that simulates output generation for tests."""

    def generate(self, **kwargs):  # pylint: disable=unused-argument
        """Simulate model output generation."""
        return "dummy_output"


@pytest.fixture
def animal_detector_fixture(monkeypatch):
    """
    Fixture for providing an AnimalDetector instance with
    dummy processor and model.
    """
    detector = AnimalDetector()
    detector.processor = DummyProcessor()
    detector.model = DummyModel()
    return detector


def test_parse_response_positive(animal_detector_fixture):
    """
    Test parse_response with a positive animal detection response.
    """
    response = (
        "Animal Detected: Yes. Type: Giraffe. "
        "Description: A giraffe is seen on the savannah."
    )
    result = animal_detector_fixture.parse_response(response)
    assert result["animal_or_not"] == 1
    # Compare in lowercase to avoid capitalization differences.
    assert result["type"].lower() == "giraffe"
    assert "giraffe" in result["text_description"].lower()


def test_parse_response_negative(animal_detector_fixture):
    """
    Test parse_response with a negative animal detection response.
    """
    response = "No animal detected in the image."
    result = animal_detector_fixture.parse_response(response)
    assert result["animal_or_not"] == 0
    assert result["type"] == ""