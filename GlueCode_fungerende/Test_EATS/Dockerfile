FROM python:3.11-slim
COPY . /app
WORKDIR /app

# Install system dependencies required by OpenCV
#RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]