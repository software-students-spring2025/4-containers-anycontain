FROM python:3.10-slim

# 1) install system libs for OpenCV
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libgl1-mesa-glx \
      libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2) install Python deps via Pipenv
COPY Pipfile    Pipfile.lock  /app/
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir pipenv \
 && pipenv install --deploy --system

RUN pip install flask-cors
# 3) copy ML client library if you’re mounting it (or bake it in)
#    COPY machine_learning_client /app/machine_learning_client

# 4) copy your backend code
COPY backend/   /app/

EXPOSE 5000

CMD ["python", "run.py"]
