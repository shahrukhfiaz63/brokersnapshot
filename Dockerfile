FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget curl unzip chromium chromium-driver && \
    rm -rf /var/lib/apt/lists/*

# Add symlinks (some systems use chromium-browser vs chromium)
RUN ln -s /usr/bin/chromium /usr/bin/chromium-browser || true

ENV PATH="/usr/lib/chromium/:${PATH}"
ENV CHROME_BIN="/usr/bin/chromium"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python", "app.py"]
