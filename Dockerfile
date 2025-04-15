FROM python:3.10-slim

# Install Chromium and driver
RUN apt-get update && \
    apt-get install -y wget curl unzip chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Set environment paths
ENV PATH="/usr/lib/chromium/:${PATH}"
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python", "app.py"]
