import random


def analyze_image(file_bytes):
    animals = ["Cat", "Dog", "Tiger", "Elephant", "Fox"]
    results = []

    for _ in range(random.randint(1, 3)):
        animal = random.choice(animals)
        confidence = round(random.uniform(0.6, 0.99), 2)
        results.append({"animal": animal, "confidence": confidence})

    return {"results": results}
