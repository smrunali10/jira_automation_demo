# Use Python 3.12 slim base image
FROM python:3.12-slim

# Install system dependencies for Playwright + xvfb-run
RUN apt-get update && apt-get install -y \
    curl wget gnupg \
    xvfb xauth \
    libnss3 libatk-bridge2.0-0 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libxshmfence1 libxext6 libxfixes3 libegl1 libfontconfig1 \
    libharfbuzz0b libpango-1.0-0 libpangocairo-1.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /tests

# Copy all project files into container
COPY . /tests

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (Chromium, Firefox, WebKit) with dependencies
RUN python -m playwright install --with-deps

# Set PYTHONPATH so Robot Framework can find custom libraries
ENV PYTHONPATH=/tests/resources

# Default command: run Robot Framework tests with xvfb-run
CMD ["xvfb-run", "robot", "-d", "results", "resources/E2E_Jira.robot"]
#CMD ["robot", "-d", "results", "resources/E2E_Jira.robot"]

