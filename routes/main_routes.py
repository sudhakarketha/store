from flask import Blueprint, render_template
from models.product import Product, Category

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    featured_products = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    return render_template('main/home.html', 
                           title='Welcome to Ketha Store', 
                           featured_products=featured_products,
                           categories=categories)

@main_bp.route('/about')
def about():
    return render_template('main/about.html', title='About Us')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html', title='Contact Us')