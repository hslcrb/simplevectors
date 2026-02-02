# Base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for PySide6 (Qt)
# libgl1-mesa-glx: OpenGL support
# libxkbcommon-x11-0: Keyboard support
# libdbus-1-3: DBus support (often needed by Qt)
# libxcb-*: X11 backend support
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-shape0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements first to leverage caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app/src

# Command to run the application
# Note: For GUI to work, you need to share the X11 socket when running:
# docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix simplevectors
CMD ["python3", "src/main.py"]
