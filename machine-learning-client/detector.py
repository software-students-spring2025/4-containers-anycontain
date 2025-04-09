import cv2
import torch
from transformers import (
    BitsAndBytesConfig,
    LlavaNextVideoForConditionalGeneration,
    LlavaNextVideoProcessor,
)


class AnimalDetector:
    """Class to perform animal detection analysis on input images using a LLaVA-based model."""

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # self.quantization_config = BitsAndBytesConfig(
        #     load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16
        # )

        self.processor = LlavaNextVideoProcessor.from_pretrained(
            "llava-hf/LLaVA-NeXT-Video-7B-hf"
        )
        self.model = LlavaNextVideoForConditionalGeneration.from_pretrained(
            "llava-hf/LLaVA-NeXT-Video-7B-hf",
            device_map="auto",
        )

    def detect(self, image_path: str) -> dict:
        """
        Detect animal presence and type in the given image.
        :param image_path: Path to the image file.
        :return: Dictionary containing detection results with keys:
                 'animal_or_not', 'type', 'text_description'
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Unable to read image from the given path.")

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is this animal?"},
                    {"type": "image"},
                ],
            },
        ]

        prompt = self.processor.apply_chat_template(
            conversation, add_generation_prompt=True
        )

        inputs = self.processor(text=[prompt], images=[image_rgb], return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=64)
        response_text = self.processor.batch_decode(outputs, skip_special_tokens=True)[
            0
        ]

        result = self.parse_response(response_text)
        return result

    @staticmethod
    def parse_response(response: str) -> dict:
        """
        Parse the raw model response into structured detection results.
        :param response: The raw text returned by the model.
        :return: A dictionary with keys 'animal_or_not', 'type', and 'text_description'.
        """
        animal_or_not = 0
        animal_type = ""
        text_description = response.strip()

        if "no animal" in response.lower():
            animal_or_not = 0
            animal_type = ""
        else:
            animal_or_not = 1
            if "type:" in response.lower():
                try:
                    parts = response.lower().split("type:")
                    type_part = parts[1].split(".")[0]
                    animal_type = type_part.strip().capitalize()
                except Exception:
                    animal_type = "Unknown"
            else:
                animal_type = "Animal Detected"

        return {
            "animal_or_not": animal_or_not,
            "type": animal_type,
            "text_description": text_description,
        }
