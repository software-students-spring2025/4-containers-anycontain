import os
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
        "text_description": text_description
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






# Sample for store_image
# if __name__ == "__main__":
#     with open("sample1.jpg", "rb") as image_file:
#         binary_data = image_file.read()
    
#     inserted_id = store_image(binary_data)
#     print("Inserted document with id:", inserted_id)


# Sample for fetch_all_pictures
# if __name__ == "__main__":
#     images = fetch_all_pictures("x.env")
#     print(f"Fetched {len(images)} images.")
#     download_images(images, output_dir="example_fetched_picture")