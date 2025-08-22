# Use the official Python image from the Docker Hub
FROM python:3.13.2

# Set the working directory in the container
WORKDIR /competitor-research-tool

# Install Firefox and Geckodriver
RUN apt-get update && apt-get install -y \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver
RUN apt-get update && apt-get install -y wget \
    && wget -q https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.30.0-linux64.tar.gz -C /usr/local/bin \
    && rm geckodriver-v0.30.0-linux64.tar.gz

# Copy the requirements file into the container
COPY requirements.txt /competitor-research-tool/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /competitor-research-tool/

# Expose the port that Streamlit will run on
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
