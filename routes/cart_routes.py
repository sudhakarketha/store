from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from models import db
from models.product import Product
from models.order import CartItem, Order, OrderItem

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart/cart.html', 
                           title='Your Cart', 
                           cart_items=cart_items,
                           total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        flash('Quantity must be positive!', 'danger')
        return redirect(url_for('product.product_detail', product_id=product_id))
    
    if product.stock < quantity:
        flash(f'Sorry, only {product.stock} items available!', 'danger')
        return redirect(url_for('product.product_detail', product_id=product_id))
    
    # Check if product already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to your cart!', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Ensure the cart item belongs to the current user
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart!', 'info')
    else:
        if quantity > cart_item.product.stock:
            flash(f'Sorry, only {cart_item.product.stock} items available!', 'danger')
            quantity = cart_item.product.stock
        
        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated!', 'success')
    
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Ensure the cart item belongs to the current user
    if cart_item.user_id != current_user.id:
        flash('Unauthorized action!', 'danger')
        return redirect(url_for('cart.view_cart'))
    
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart!', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/checkout')
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'info')
        return redirect(url_for('product.all_products'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart/checkout.html', 
                           title='Checkout', 
                           cart_items=cart_items,
                           total=total)

@cart_bp.route('/place-order', methods=['POST'])
@login_required
def place_order():
    # Get all cart items for the current user
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'info')
        return redirect(url_for('product.all_products'))
    
    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Create a new order
    order = Order(
        user_id=current_user.id,
        total_price=total,
        status='pending'
    )
    db.session.add(order)
    db.session.flush()  # This assigns an ID to the order
    
    # Create order items and update product stock
    for cart_item in cart_items:
        # Check if enough stock
        if cart_item.product.stock < cart_item.quantity:
            flash(f'Sorry, not enough stock for {cart_item.product.name}!', 'danger')
            return redirect(url_for('cart.view_cart'))
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.session.add(order_item)
        
        # Update product stock
        cart_item.product.stock -= cart_item.quantity
        
        # Remove cart item
        db.session.delete(cart_item)
    
    # Commit all changes
    db.session.commit()
    
    flash('Your order has been placed successfully!', 'success')
    return redirect(url_for('main.home'))