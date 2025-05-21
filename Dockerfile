# Use a stable Python image
FROM python:3.12

# Set environment variables to prevent Python from writing bytecode and ensure unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies required for Google Chrome and other utilities
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    wget \
    gnupg2 \
    curl \
    ca-certificates \
    sudo \
    libx11-6 \
    libnss3 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libgtk-3-0 \
    libgbm1 \
    xdg-utils \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y wget gnupg2 \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy application files (including requirements.txt) to the container
COPY . /app
# Install Google Chrome


# Download ChromeDriver and unzip it to a folder within the app
RUN wget https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.141/linux64/chromedriver-linux64.zip -P /tmp \
    && unzip /tmp/chromedriver-linux64.zip -d /app/chromedriver/ \
    && mv /app/chromedriver/chromedriver-linux64/chromedriver /app/chromedriver/chromedriver \
    && chmod +x /app/chromedriver/chromedriver \
    && rm -rf /tmp/chromedriver-linux64.zip /app/chromedriver/chromedriver-linux64

# Add chromedriver to PATH
ENV PATH="/app/chromedriver:${PATH}"

# Install Python dependencies including Django and watchdog
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt \
    && pip install watchdog

# Set executable permissions for the entrypoint script
RUN chmod +x /app/docker-entrypoint.sh

# Define the entrypoint for the container
ENTRYPOINT ["bash", "/app/docker-entrypoint.sh"]


