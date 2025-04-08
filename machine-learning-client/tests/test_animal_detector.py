import pytest
from animal_detector import AnimalDetector


class DummyProcessor:
    def __init__(self):
        pass

    def __call__(self, images, return_tensors):

        return {"dummy": "tensor"}

    def batch_decode(self, outputs, skip_special_tokens):
        return ["Animal Detected: Yes. Type: Elephant. Description: Detected an elephant in the image."]


class DummyModel:
    def generate(self, **kwargs):
        return "dummy_output"


@pytest.fixture
def animal_detector(monkeypatch):
    detector = AnimalDetector()
    detector.processor = DummyProcessor()
    detector.model = DummyModel()
    return detector


def test_parse_response_positive(animal_detector):
    response = "Animal Detected: Yes. Type: Giraffe. Description: A giraffe is seen on the savannah."
    result = animal_detector.parse_response(response)
    assert result["animal_or_not"] == 1
    assert result["type"].lower() == "giraffe"
    assert "giraffe" in result["text_description"].lower()


def test_parse_response_negative(animal_detector):
    response = "No animal detected in the image."
    result = animal_detector.parse_response(response)
    assert result["animal_or_not"] == 0
    assert result["type"] == ""