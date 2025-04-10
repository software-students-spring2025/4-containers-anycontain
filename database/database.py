import os
import numpy as np
import cv2
from pymongo import MongoClient
from bson.binary import Binary
from dotenv import load_dotenv

def store_image(binary_data, animal_or_not=0, image_type="", text_description="", env_file="x.env"):

    load_dotenv(env_file)
    connection_string = os.environ.get("MONGODB_URI")
    
    client = MongoClient(connection_string)
    db = client.get_database("AnimalDetector")
    
    bson_binary = Binary(binary_data)
    
    document = {
        "image_data": bson_binary,
        "animal_or_not": animal_or_not,
        "type": image_type,
        "text_description": text_description,
        "processed": False
    }
    result = db.pictures.insert_one(document)
    return result.inserted_id


def fetch_all_pictures(env_file="x.env"):

    load_dotenv(env_file)
    connection_string = os.environ.get("MONGODB_URI")

    client = MongoClient(connection_string)
    db = client.get_database("AnimalDetector")

    documents = list(db.pictures.find())
    
    images = []
    for doc in documents:
        binary_data = doc.get("image_data")
        if binary_data is not None:
            nparr = np.frombuffer(binary_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            images.append(image)
    
    return images

def download_images(images, output_dir="example_fetched_picture"):
 
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, image in enumerate(images):
        filename = os.path.join(output_dir, f"image_{idx}.jpg")
        cv2.imwrite(filename, image)
        print(f"Saved {filename}")

def fetch_id_and_image_data(env_file="x.env"):
    
    load_dotenv(env_file)
    connection_string = os.environ.get("MONGODB_URI")

    client = MongoClient(connection_string)
    db = client.get_database("AnimalDetector")

    
    cursor = db.pictures.find({}, {"_id": 1, "image_data": 1})
    
    results = []
    for doc in cursor:
        results.append({
            "_id": doc["_id"],
            "image_data": doc["image_data"]
        })
    
    return results

def update_classification(document_id, animal_or_not, image_type, text_description, env_file="x.env"):
    
    load_dotenv(env_file)
    connection_string = os.environ.get("MONGODB_URI")

    client = MongoClient(connection_string)
    db = client.get_database("AnimalDetector")

    update_fields = {
        "animal_or_not": animal_or_not,
        "type": image_type,
        "text_description": text_description,
        "processed": processed  # update the processed flag
    }
    result = db.pictures.update_one(
        {"_id": document_id},
        {"$set": update_fields}
    )

    return result.modified_count

def _id_repr(_id):
    return str(_id)



