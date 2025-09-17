# Ketha Store

A full-featured e-commerce application similar to Amazon, built with Python.

## Features

- Product browsing and searching
- User authentication and profiles
- Shopping cart functionality
- Secure checkout process
- Order history and tracking
- Product reviews and ratings
- Admin dashboard for product management

## Tech Stack

- **Backend**: Python, Flask/Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite/PostgreSQL
- **Authentication**: Flask-Login/Django Auth
- **Payment Processing**: Stripe
- **Deployment**: Docker, Heroku/AWS

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (venv or conda)

### Installation

1. Clone the repository
2. Create and activate a virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables
5. Run the application
   ```
   python app.py  # For Flask
   # OR
   python manage.py runserver  # For Django
   ```

## Deployment on Render

This guide explains how to deploy the Ketha Store application on Render with a MySQL database hosted on Clever Cloud.

### Prerequisites

1. A Render account (https://render.com)
2. A Clever Cloud account with MySQL database (already set up)
3. The MySQL database URL from Clever Cloud

### Deployment Steps

#### Option 1: Using render.yaml (Recommended)

1. **Push your code to a Git repository**

   - Make sure your code is in a Git repository (GitHub, GitLab, etc.)
   - The repository should include the `render.yaml` configuration file

2. **Create a new service on Render using Blueprint**

   - Sign in to your Render account
   - Click on "New" and select "Blueprint"
   - Connect your repository
   - Render will automatically detect the `render.yaml` file and configure your service

3. **Set the DATABASE_URI environment variable**

   - After the service is created, go to the Environment settings
   - Add your MySQL connection string from Clever Cloud as the `DATABASE_URI` value

#### Option 2: Manual Configuration

1. **Create a new Web Service on Render**

   - Sign in to your Render account
   - Click on "New" and select "Web Service"
   - Connect your GitHub repository or upload your code directly

2. **Configure the Web Service**

   - **Name**: Choose a name for your service (e.g., ketha-store)
   - **Runtime**: Select "Python"
   - **Build Command**: `chmod +x ./build.sh && ./build.sh`
   - **Start Command**: `gunicorn app:app`

3. **Set Environment Variables**

   Add the following environment variables in the Render dashboard:

   - `SECRET_KEY`: A secure random string for Flask
   - `FLASK_ENV`: Set to `production`
   - `FLASK_DEBUG`: Set to `False`
   - `DATABASE_URI`: Your MySQL connection string from Clever Cloud

4. **Deploy the Application**

   - Click "Create Web Service"
   - Render will automatically build and deploy your application

5. **Verify Deployment**

   - Once deployment is complete, click on the URL provided by Render to access your application
   - Verify that the application is working correctly and can connect to the database

### Troubleshooting

- **Database Connection Issues**: Ensure that the DATABASE_URI environment variable is correctly set and that the database is accessible from Render's servers.
- **Build Failures**: Check the build logs for any errors. Common issues include missing dependencies or incorrect file paths.
   - If you encounter Pillow installation errors, the application now uses a pre-built Pillow wheel (version 8.4.0) which is installed separately in the build script to avoid compilation issues.
- **Application Errors**: Check the application logs in the Render dashboard for detailed error messages.

## Project Structure

- `/app` - Main application code
- `/templates` - HTML templates
- `/static` - CSS, JavaScript, and image files
- `/models` - Database models
- `/routes` or `/views` - Application routes/views
- `/docs` - Documentation files