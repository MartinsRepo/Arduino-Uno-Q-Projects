FROM python:3.12-slim

# Updated system libs for OpenCV (Debian Trixie/Bookworm compatibility)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    mc \
    nano \
    ffmpeg \
    v4l-utils \
    x264 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mv "env" ".env"

EXPOSE 5000
CMD ["python", "face_service.py"]
#CMD ["/bin/bash"]
