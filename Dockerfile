FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget curl unzip chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

# Set working directory and copy app
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port & run
EXPOSE 8080
CMD ["python", "app.py"]
