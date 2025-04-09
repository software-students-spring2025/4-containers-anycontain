"""Module for simulating animal detection from an image.

Note:
    This is a fake model. The parameter file_bytes is accepted but not used.
"""

import random


def analyze_image(_file_bytes):
    """
    Simulate analyzing an image and return fake detection results.

    Args:
        file_bytes (bytes): The raw image bytes. (Unused in simulation)

    Returns:
        dict: A dictionary with a "results" key containing a list of detected animals.
    """
    animals = ["Cat", "Dog", "Tiger", "Elephant", "Fox"]
    results = []
    for _ in range(random.randint(1, 3)):
        animal = random.choice(animals)
        confidence = round(random.uniform(0.6, 0.99), 2)
        results.append({"animal": animal, "confidence": confidence})
    return {"results": results}
