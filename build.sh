#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip

# Install system dependencies for Pillow
apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    zlib1g-dev || true

# Install Pillow separately with binary option
pip install --only-binary=:all: Pillow==8.4.0

# Install other requirements
pip install -r requirements.txt

# Run database migrations
flask db init || true
flask db migrate
flask db upgrade