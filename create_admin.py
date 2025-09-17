from app import app, db
from models.user import User

# Create admin user
def create_admin_user(username, email, password):
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
            # If user exists but is not admin, make them admin
            if not existing_user.is_admin:
                existing_user.is_admin = True
                db.session.commit()
                print(f"User {username} has been upgraded to admin.")
            return
        
        # Create new admin user
        admin = User(username=username, email=email, is_admin=True)
        admin.password = password  # This will hash the password
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user {username} created successfully!")

if __name__ == '__main__':
    username = 'admin'
    email = 'admin@example.com'
    password = 'adminpassword'
    
    create_admin_user(username, email, password)
    print("\nYou can now login with:")
    print(f"Email: {email}")
    print(f"Password: {password}")