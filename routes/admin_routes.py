from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from models import db
from models.product import Product, Category
from models.order import Order
from models.user import User
from forms.product_forms import ProductForm, CategoryForm

admin_bp = Blueprint('admin', __name__)

# Admin access decorator
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def admin_dashboard():
    product_count = Product.query.count()
    order_count = Order.query.count()
    user_count = User.query.count()
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           title='Admin Dashboard',
                           product_count=product_count,
                           order_count=order_count,
                           user_count=user_count,
                           recent_orders=recent_orders)

# Product Management
@admin_bp.route('/products')
@login_required
@admin_required
def manage_products():
    products = Product.query.all()
    return render_template('admin/products.html', 
                           title='Manage Products',
                           products=products)

@admin_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_product():
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category_id=form.category_id.data
        )
        
        # Handle image upload
        if form.image.data:
            # Save image logic here
            pass
        
        db.session.add(product)
        db.session.commit()
        flash('Product has been created!', 'success')
        return redirect(url_for('admin.manage_products'))
    
    return render_template('admin/product_form.html', 
                           title='New Product',
                           form=form,
                           legend='New Product')

@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category_id = form.category_id.data
        
        # Handle image upload
        if form.image.data:
            # Save image logic here
            pass
        
        db.session.commit()
        flash('Product has been updated!', 'success')
        return redirect(url_for('admin.manage_products'))
    elif request.method == 'GET':
        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
        form.stock.data = product.stock
        form.category_id.data = product.category_id
    
    return render_template('admin/product_form.html', 
                           title='Edit Product',
                           form=form,
                           legend='Edit Product')

@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted!', 'success')
    return redirect(url_for('admin.manage_products'))

# Category Management
@admin_bp.route('/categories')
@login_required
@admin_required
def manage_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', 
                           title='Manage Categories',
                           categories=categories)

@admin_bp.route('/categories/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_category():
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Category has been created!', 'success')
        return redirect(url_for('admin.manage_categories'))
    
    return render_template('admin/category_form.html', 
                           title='New Category',
                           form=form,
                           legend='New Category')

@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash('Category has been updated!', 'success')
        return redirect(url_for('admin.manage_categories'))
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    
    return render_template('admin/category_form.html', 
                           title='Edit Category',
                           form=form,
                           legend='Edit Category')

@admin_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted!', 'success')
    return redirect(url_for('admin.manage_categories'))

# Order Management
@admin_bp.route('/orders')
@login_required
@admin_required
def manage_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('admin/orders.html', 
                           title='Manage Orders',
                           orders=orders)

@admin_bp.route('/orders/<int:order_id>')
@login_required
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', 
                           title=f'Order #{order.id}',
                           order=order)

@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    
    if status in ['pending', 'shipped', 'delivered', 'cancelled']:
        order.status = status
        db.session.commit()
        flash(f'Order status updated to {status}!', 'success')
    else:
        flash('Invalid status!', 'danger')
    
    return redirect(url_for('admin.order_detail', order_id=order.id))