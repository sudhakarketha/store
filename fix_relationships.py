import os
import sys
from flask import Flask
from models import db
from sqlalchemy import text

# Create a minimal Flask app
app = Flask(__name__)

# Ensure instance directory exists
os.makedirs('instance', exist_ok=True)

# Configure the SQLite database with absolute path
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'ketha_store.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

def fix_relationships():
    with app.app_context():
        try:
            # Fix the Review-Product relationship
            # First, check if there are any reviews with invalid product_ids
            with db.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT r.id, r.product_id FROM review r 
                    LEFT JOIN product p ON r.product_id = p.id 
                    WHERE p.id IS NULL
                """))
                invalid_reviews = result.fetchall()
                
                if invalid_reviews:
                    print(f"Found {len(invalid_reviews)} reviews with invalid product_ids")
                    for review in invalid_reviews:
                        print(f"Deleting review {review[0]} with invalid product_id {review[1]}")
                        conn.execute(text(f"DELETE FROM review WHERE id = {review[0]}"))
                    conn.commit()
                    print("Invalid reviews deleted.")
                else:
                    print("No reviews with invalid product_ids found.")
                
                # Check for orphaned order items
                result = conn.execute(text("""
                    SELECT oi.id, oi.product_id FROM order_item oi 
                    LEFT JOIN product p ON oi.product_id = p.id 
                    WHERE p.id IS NULL
                """))
                invalid_order_items = result.fetchall()
                
                if invalid_order_items:
                    print(f"Found {len(invalid_order_items)} order items with invalid product_ids")
                    for item in invalid_order_items:
                        print(f"Deleting order item {item[0]} with invalid product_id {item[1]}")
                        conn.execute(text(f"DELETE FROM order_item WHERE id = {item[0]}"))
                    conn.commit()
                    print("Invalid order items deleted.")
                else:
                    print("No order items with invalid product_ids found.")
                
                # Check for orphaned cart items
                result = conn.execute(text("""
                    SELECT ci.id, ci.product_id FROM cart_item ci 
                    LEFT JOIN product p ON ci.product_id = p.id 
                    WHERE p.id IS NULL
                """))
                invalid_cart_items = result.fetchall()
                
                if invalid_cart_items:
                    print(f"Found {len(invalid_cart_items)} cart items with invalid product_ids")
                    for item in invalid_cart_items:
                        print(f"Deleting cart item {item[0]} with invalid product_id {item[1]}")
                        conn.execute(text(f"DELETE FROM cart_item WHERE id = {item[0]}"))
                    conn.commit()
                    print("Invalid cart items deleted.")
                else:
                    print("No cart items with invalid product_ids found.")
                
            print("\nDatabase relationships fixed successfully!")
            
        except Exception as e:
            print(f"Error fixing relationships: {e}")

if __name__ == '__main__':
    fix_relationships()