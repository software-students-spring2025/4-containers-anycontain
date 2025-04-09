import sys

from machine_learning_client.database import store_image, update_classification
from machine_learning_client.detector import AnimalDetector


def main():
    image_path = "sample.png"

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
    except FileNotFoundError:
        print(f"Sample image '{image_path}' not found.", file=sys.stderr)
        return

    inserted_id = store_image(
        image_bytes,
        animal_or_not=0,
        image_type="",
        text_description="Raw image",
        env_file="x.env",
    )
    print(f"Stored image with id: {inserted_id}")

    detector = AnimalDetector()
    try:
        result = detector.detect(image_path)
    except Exception as e:
        print(f"Error during detection: {e}", file=sys.stderr)
        return

    print("Detection result:", result)

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
