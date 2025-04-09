import pytest
from machine_learning_client.detector import AnimalDetector


class DummyProcessor:
    """Dummy processor to simulate model processing for tests."""

    def __call__(self, images, return_tensors):
        """Simulate processing of images."""
        return {"dummy": "tensor"}

    def batch_decode(self, _outputs, _skip_special_tokens):
        """Simulate decoding of model outputs."""
        return [
            "Animal Detected: Yes. Type: Elephant. Description: Detected an elephant in the image."
        ]


class DummyModel:
    """Dummy model that simulates output generation for tests."""

    def generate(self, **_kwargs):
        """Simulate model output generation."""
        return "dummy_output"


@pytest.fixture
def dummy_detector():
    """
    Fixture to provide an AnimalDetector instance with dummy processor and model.
    """
    instance = AnimalDetector()
    instance.processor = DummyProcessor()
    instance.model = DummyModel()
    return instance


def test_parse_response_positive(dummy_detector):
    """
    Test parse_response with a positive animal detection response.
    """
    response = (
        "Animal Detected: Yes. Type: Giraffe. Description: A giraffe is seen on the savannah."
    )
    result = dummy_detector.parse_response(response)
    assert result["animal_or_not"] == 1
    assert result["type"].lower() == "giraffe"
    assert "giraffe" in result["text_description"].lower()


def test_parse_response_negative(dummy_detector):
    """
    Test parse_response with a negative animal detection response.
    """
    response = "No animal detected in the image."
    result = dummy_detector.parse_response(response)
    assert result["animal_or_not"] == 0
    assert result["type"] == ""