import sys
import base64
import cv2
from machine_learning_client.database import store_image, update_classification
from machine_learning_client.detector import AnimalDetector
from openai import OpenAI

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def detect_with_openai(image_path):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image? If there is an animal, mention its type; otherwise, say 'no animal'."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ],
        max_tokens=100,
    )
    response_text = response.choices[0].message.content.strip()
    return response_text


def main():
    use_openai = "--openai" in sys.argv
    image_path = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "sample.png"

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    except FileNotFoundError:
        print(f"Image '{image_path}' not found.", file=sys.stderr)
        return

    inserted_id = store_image(
        image_bytes,
        animal_or_not=0,
        image_type="",
        text_description="Raw image",
        env_file="x.env",
    )
    print(f"Stored image with id: {inserted_id}")

    if use_openai:
        try:
            response_text = detect_with_openai(image_path)
            print("OpenAI GPT-4o detection result:", response_text)
            result = AnimalDetector.parse_response(response_text)
        except Exception as e:
            print(f"Error during OpenAI detection: {e}", file=sys.stderr)
            return
    else:
        detector = AnimalDetector()
        try:
            result = detector.detect(image_path)
            print("Local model detection result:", result)
        except Exception as e:
            print(f"Error during local detection: {e}", file=sys.stderr)
            return

    updated_count = update_classification(
        inserted_id,
        animal_or_not=result["animal_or_not"],
        image_type=result["type"],
        text_description=result["text_description"],
        env_file="x.env",
    )
    print(f"Updated {updated_count} document(s) with classification result.")


if __name__ == "__main__":
    main()