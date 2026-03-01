FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (needed for some Python libraries like hdbscan)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (to cache the heavy install step)
COPY requirements.txt .

# Install Python packages and download the spaCy model
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm

# Copy the rest of your project code
COPY . .

# Run main.py when the container starts
CMD ["python", "main.py"]