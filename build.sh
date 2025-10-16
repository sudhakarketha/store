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

# Install Werkzeug explicitly for compatibility with Flask-Login
pip install werkzeug==2.3.7

# Install other requirements
pip install -r requirements.txt

# Create static directories if they don't exist
mkdir -p static/product_images
chmod -R 755 static

# Copy default product images if they don't exist
if [ ! -f static/product_images/default_product.jpg ]; then
    cp -f static/product_images/default_product.jpg.sample static/product_images/default_product.jpg || echo "No default jpg sample found"
fi
if [ ! -f static/product_images/default_product.svg ]; then
    cp -f static/product_images/default_product.svg.sample static/product_images/default_product.svg || echo "No default svg sample found"
fi

# Create sample default images if they don't exist
if [ ! -f static/product_images/default_product.jpg ] && [ ! -f static/product_images/default_product.svg ]; then
    echo "<svg width='200' height='200' xmlns='http://www.w3.org/2000/svg'><rect width='200' height='200' fill='#f0f0f0'/><text x='50%' y='50%' font-family='Arial' font-size='20' text-anchor='middle' dominant-baseline='middle' fill='#999'>No Image</text></svg>" > static/product_images/default_product.svg
    cp static/product_images/default_product.svg static/product_images/default_product.jpg
fi

# Create no_image.svg if it doesn't exist
if [ ! -f "static/product_images/no_image.svg" ]; then
    echo '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" fill="#f8f9fa" /><rect x="1" y="1" width="198" height="198" fill="none" stroke="#dee2e6" stroke-width="2" /><text x="100" y="100" font-family="Arial, sans-serif" font-size="16" text-anchor="middle" dominant-baseline="middle" fill="#6c757d">No Image</text><path d="M70,80 L130,120 M130,80 L70,120" stroke="#dee2e6" stroke-width="2" /></svg>' > static/product_images/no_image.svg
fi

# Run database migrations
flask db init || true
flask db migrate
flask db upgrade