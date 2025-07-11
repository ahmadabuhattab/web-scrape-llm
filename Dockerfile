FROM python:3.11-slim

# 1. Install system libs for Playwright + Chromium
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      fonts-liberation \
      libasound2 \
      libatk1.0-0 \
      libcups2 \
      libdbus-1-3 \
      libdrm2 \
      libexpat1 \
      libgbm1 \
      libglib2.0-0 \
      libgtk-3-0 \
      libnspr4 \
      libnss3 \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libx11-6 \
      libxcomposite1 \
      libxcursor1 \
      libxdamage1 \
      libxext6 \
      libxfixes3 \
      libxi6 \
      libxrandr2 \
      libxrender1 \
      libxshmfence1 \
      libxtst6 \
      libdbus-glib-1-2 && \
    rm -rf /var/lib/apt/lists/*

# 2. Set up Python environment
ENV PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app
COPY requirements.txt .

# 3. Install Python deps and the browser
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install chromium

# 4. Copy code and default command
COPY . .
CMD ["uvicorn", "api_main:app", "--host", "0.0.0.0", "--port", "8000"]
