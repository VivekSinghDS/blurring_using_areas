FROM python:3.8.8



RUN pip install cmake
RUN pip install dlib
RUN pip install face_recognition fastapi uvicorn opencv-python

RUN useradd -ms /bin/bash appuser
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && rm -rf /var/lib/apt/lists/*

WORKDIR /home/appuser
USER appuser
COPY api_file_blurring.py ./
COPY testcase_blur.py ./


CMD ["python", "api_file_blurring.py"]