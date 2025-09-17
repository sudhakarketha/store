import os
from dotenv import load_dotenv
import pymysql
import sys

# Load environment variables
load_dotenv()

# Get database URI from environment
database_uri = os.getenv('DATABASE_URI')

if not database_uri:
    print("ERROR: DATABASE_URI environment variable not set.")
    sys.exit(1)

# Parse the database URI
# Format: mysql://username:password@host:port/database
try:
    # Remove mysql:// prefix
    db_info = database_uri.replace('mysql://', '')
    # Split username:password and host:port/database
    auth, connection = db_info.split('@')
    # Split username and password
    username, password = auth.split(':')
    # Split host:port and database
    host_port, database = connection.split('/')
    # Split host and port
    if ':' in host_port:
        host, port = host_port.split(':')
        port = int(port)
    else:
        host = host_port
        port = 3306  # Default MySQL port
    
    print(f"Attempting to connect to MySQL database at {host}:{port}...")
    
    # Try to establish a connection
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=database,
        port=port
    )
    
    print("SUCCESS: Connected to the MySQL database!")
    print(f"Database: {database}")
    
    # Test query
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"MySQL Version: {version[0]}")
    
    connection.close()
    print("Connection closed.")
    
except Exception as e:
    print(f"ERROR: Failed to connect to the database: {e}")
    sys.exit(1)