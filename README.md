[![lint-free](https://github.com/software-students-spring2025/4-containers-anycontain/actions/workflows/lint.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-anycontain/actions/workflows/lint.yml)
[![Python CI](https://github.com/software-students-spring2025/4-containers-anycontain/actions/workflows/ci.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-anycontain/actions/workflows/ci.yml)
# Containerized App Exercise

![Project Icon](/images/icon.png)
# Animal Detection for Wildlife Protection

This project implements a itegrated system with a website interface and machine learning client that detects the presence and type of animals in images for wild life protection. The ML client get the images input of user from the web app, analyzes them using a finetuned LLaVA-based model or call gpt api, stores the raw image data and detection metadata into a MongoDB database, and then the web app will read the result and display it. For testing, you can collect a bunch of images with your camera and test its ability to detect animals in the city


## Team members (In Alphabetical Order)



[**Allen Ni**](https://github.com/AllenNi66/)  

[**Jason Lin**](https://github.com/JasonLIN0226/) 

[**Hans Yin**](https://github.com/Hans-Yin/)

[**Zifan Zhao**](https://github.com/Exiam6/)

## Environment Setup

### Prerequisites

- **Python 3.11** installed on your system.
- [Pipenv](https://pipenv.pypa.io/en/latest/install/) installed globally.
- A MongoDB instance. (For local testing, you can run MongoDB in a Docker container or use your local installation. For production, consider using MongoDB Atlas.)

### Steps to Set Up the Environment

1. **Clone the Repository:**

   ```bash
   git clone <https://github.com/software-students-spring2025/4-containers-anycontain.git>
   cd <4-containers-anycontain>
   ```

2. **Install the Pipenv Environment:** 
   ```bash
   pipenv install --dev
   ```


## Example Usage
### To run with the default sample image:
    python machine_learning_client/main.py

### To run with a custom image collected with your own camera:
    python machine_learning_client/main.py images/sample.png



## Getting Started with Docker Compose

1. **Place the provided `.env` file**  
   Please contact the Anycontain team to get the `x.env` file. Move the `x.env` file you received into the project root (the same directory as `docker-compose.yml`), `/web-app` and `/machine_learning_client`.

2. **Launch all services**  
    Note the build might take around 6 minutes
   ```bash
   docker compose up --build
   ```

3. **Access the dashboard**  
   Open your browser and go to:  
   ```text
   http://localhost
   ```
   You can also use
   ```bash
   curl -F "file=@path_to_sensor_image.jpg" http://localhost:5114/upload
   ```

4. **Stop the stack**  
   ```bash
   docker-compose down
   ```

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.
