FROM python:3.10-slim

# 1) Install OpenCV native libs (if you need cv2)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) Install your Pipfile deps
COPY Pipfile Pipfile.lock /app/
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir pipenv \
 && pipenv install --deploy --system

# 3) Copy your code
COPY . /app

# 4) Quick‐and‐dirty: make /app a package named machine_learning_client
RUN ln -s /app /app/machine_learning_client

# 5) (Optional) install your project so tests etc. can pick it up
#    e.g. pip install --no-cache-dir -e .  

CMD ["python", "main.py"]
