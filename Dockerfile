# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install libX11 and other dependencies
RUN apt-get update && \
    apt-get install -y libx11-6 libxext-dev ffmpeg libsm6 libxext6 libgl1-mesa-glx xvfb && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/
COPY *.py /app/
COPY assets /app/
COPY .streamlit /app/
#COPY stls /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 8521 available to the world outside this container
EXPOSE 8521

# Run app.py when the container launches
CMD ["streamlit", "run", "mega_shaper_app.py", "--server.port", "8521"]
