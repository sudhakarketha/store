from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models import db
from models.product import Product, Category, Review
from forms.product_forms import ReviewForm

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def all_products():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search_query = request.args.get('search', '')
    
    if category_id:
        products = Product.query.filter_by(category_id=category_id)
    elif search_query:
        products = Product.query.filter(Product.name.contains(search_query) | 
                                       Product.description.contains(search_query))
    else:
        products = Product.query
    
    products = products.order_by(Product.created_at.desc()).paginate(page=page, per_page=12)
    categories = Category.query.all()
    
    return render_template('product/all_products.html', 
                           title='All Products', 
                           products=products.items,
                           pagination=products,
                           categories=categories,
                           search_query=search_query)

@product_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    return render_template('product/product_detail.html', 
                           title=product.name, 
                           product=product,
                           form=form)

@product_bp.route('/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()
    
    if form.validate_on_submit():
        review = Review(
            rating=form.rating.data,
            comment=form.comment.data,
            product=product,
            author=current_user
        )
        db.session.add(review)
        db.session.commit()
        flash('Your review has been added!', 'success')
    
    return redirect(url_for('product.product_detail', product_id=product.id))