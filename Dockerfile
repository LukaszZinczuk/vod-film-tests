FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Playwright
RUN apt-get update && apt-get install -y \
  wget \
  gnupg \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Command to run tests
CMD ["pytest", "tests/", "-v", "--html=reports/report.html", "--self-contained-html"]