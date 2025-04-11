import os
import cv2
import base64
from openai import OpenAI
from dotenv import load_dotenv

class AnimalDetector:
    """Class to perform animal detection analysis using either local LLaVA-based model or OpenAI GPT-4o."""

    def __init__(self, use_openai=False):
        load_dotenv(os.path.join(os.path.dirname(__file__), '/app/machine_learning_client/x.env'))
        self.use_openai = use_openai

        if not self.use_openai:
            import torch
            from transformers import LlavaNextVideoProcessor, LlavaNextVideoForConditionalGeneration
            self.device = "cpu" if os.getenv("FORCE_CPU") else ("cuda" if torch.cuda.is_available() else "cpu")
            self.processor = LlavaNextVideoProcessor.from_pretrained(
                "llava-hf/LLaVA-NeXT-Video-7B-hf"
            )
            self.model = LlavaNextVideoForConditionalGeneration.from_pretrained(
                "llava-hf/LLaVA-NeXT-Video-7B-hf", device_map="auto"
            )
        else:
            self.client = OpenAI()

    def detect(self, image_path: str) -> dict:

        if self.use_openai:
            return self.detect_with_openai(image_path)
        else:
            return self.detect_local(image_path)

    def detect_local(self, image_path: str) -> dict:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Unable to read image from the given path.")

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is this animal? If no animal, say no animal."},
                    {"type": "image"},
                ],
            }
        ]

        prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)
        inputs = self.processor(text=[prompt], images=[image_rgb], return_tensors="pt")

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=64)

        response_text = self.processor.batch_decode(outputs, skip_special_tokens=True)[0]
        return self.parse_response(response_text)

    def detect_with_openai(self, image_path: str) -> dict:
        base64_image = self.encode_image(image_path)

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image? If animal, mention type. Else, say 'no animal'."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
            max_tokens=100,
        )

        response_text = response.choices[0].message.content.strip()
        return self.parse_response(response_text)

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @staticmethod
    def parse_response(response: str) -> dict:
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