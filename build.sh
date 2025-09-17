#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run database migrations
flask db init || true
flask db migrate
flask db upgrade