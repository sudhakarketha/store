import os
import sys
from flask import Flask
from models import db
from models.product import Product, Category, Review
from models.order import Order, OrderItem, CartItem
from models.user import User

# Create a minimal Flask app
app = Flask(__name__)

# Ensure instance directory exists
os.makedirs('instance', exist_ok=True)

# Configure the SQLite database with absolute path
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'ketha_store.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Print the database path for debugging
print(f"Using database at: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")


# Initialize the database with the app
db.init_app(app)

# Function to verify and update the database schema
def verify_and_update_schema():
    with app.app_context():
        # Check if the original_price column exists in the Product table
        try:
            # Try to query a product with original_price
            product = Product.query.first()
            if product:
                print(f"Original price value: {product.original_price}")
                print("original_price column exists in the database.")
            else:
                print("No products found in the database.")
        except Exception as e:
            print(f"Error accessing original_price: {e}")
            print("The original_price column might not exist in the database.")
            print("Attempting to add the column...")
            
            # Add the original_price column if it doesn't exist
            try:
                with db.engine.connect() as conn:
                    conn.execute("ALTER TABLE product ADD COLUMN original_price FLOAT DEFAULT 0")
                    print("Column added successfully!")
            except Exception as e:
                print(f"Error adding column: {e}")

        # Verify all relationships are properly set up
        print("\nVerifying relationships:")
        try:
            # Check Product-Review relationship
            product = Product.query.first()
            if product:
                print(f"Product {product.id} has {len(product.reviews)} reviews")
                print(f"Product {product.id} has {len(product.order_items)} order items")
                print(f"Product {product.id} has {len(product.cart_items)} cart items")
            
            # Check Review-Product relationship
            review = Review.query.first()
            if review:
                print(f"Review {review.id} is for product {review.product_id}")
        except Exception as e:
            print(f"Error verifying relationships: {e}")

if __name__ == '__main__':
    verify_and_update_schema()