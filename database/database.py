import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

def main():
    # Optionally load environment variables from a .env file
    load_dotenv("x.env")
    
    # Use your provided MongoDB URI with the default database name 'AnimalDetector'
    mongodb_uri = "mongodb+srv://yn2178:00000000@cluster0.mkz5hkh.mongodb.net/AnimalDetector?retryWrites=true&w=majority"
    
    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    # Use the 'AnimalDetector' database (this will be created if it doesn't exist)
    db = client["AnimalDetector"]

    # Example 1: Create an 'animals' collection with sample animal data
    animals = db.animals
    # Clear existing data (for testing purposes)
    animals.delete_many({})
    animals_data = [
        {"name": "Deer", "reminder": "Stay calm and do not disturb."},
        {"name": "Bear", "reminder": "Keep a safe distance and alert authorities."},
        {"name": "Fox", "reminder": "Observe quietly."}
    ]
    animal_result = animals.insert_many(animals_data)
    print("Inserted animal records:", animal_result.inserted_ids)

    # Example 2: Create an 'images' collection that stores image recognition data
    images = db.images
    images.delete_many({})
    sample_images = [
        {
            "image": "photo_001.jpg",  # image filename or URL
            "is_animal": True,         # indicates animal presence
            "species": "Deer",         # the species identified
            "description": "A calm deer standing in the forest.",
            "upload_time": datetime.utcnow().isoformat()
        },
        {
            "image": "photo_002.jpg",
            "is_animal": False,
            "species": "",
            "description": "An empty scene with no animal present.",
            "upload_time": datetime.utcnow().isoformat()
        },
        {
            "image": "photo_003.jpg",
            "is_animal": True,
            "species": "Bear",
            "description": "A wild bear roaming in its natural habitat.",
            "upload_time": datetime.utcnow().isoformat()
        }
    ]
    image_result = images.insert_many(sample_images)
    print("Inserted image records:", image_result.inserted_ids)

if __name__ == "__main__":
    main()
