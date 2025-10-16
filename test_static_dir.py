import os
import sys
from flask import Flask

app = Flask(__name__)

def test_static_directory():
    # Get the app's root path
    root_path = app.root_path
    print(f"App root path: {root_path}")
    
    # Check if static directory exists
    static_path = os.path.join(root_path, 'static')
    print(f"Static path: {static_path}")
    print(f"Static directory exists: {os.path.exists(static_path)}")
    
    # Check if product_images directory exists
    product_images_path = os.path.join(static_path, 'product_images')
    print(f"Product images path: {product_images_path}")
    print(f"Product images directory exists: {os.path.exists(product_images_path)}")
    
    # Try to create a test file in the product_images directory
    test_file_path = os.path.join(product_images_path, 'test_file.txt')
    try:
        with open(test_file_path, 'w') as f:
            f.write('Test file for checking write permissions')
        print(f"Successfully created test file: {test_file_path}")
        
        # Read the file back to verify
        with open(test_file_path, 'r') as f:
            content = f.read()
        print(f"Successfully read test file. Content: {content}")
        
        # Clean up
        os.remove(test_file_path)
        print(f"Successfully removed test file")
    except Exception as e:
        print(f"Error working with test file: {e}")
    
    # List all files in the product_images directory
    print("\nFiles in product_images directory:")
    try:
        for file in os.listdir(product_images_path):
            file_path = os.path.join(product_images_path, file)
            print(f"  {file} - {'Directory' if os.path.isdir(file_path) else 'File'} - {os.path.getsize(file_path)} bytes")
    except Exception as e:
        print(f"Error listing files: {e}")

if __name__ == '__main__':
    test_static_directory()