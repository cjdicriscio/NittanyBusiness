from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nittanybusiness.db'
app.config['SQLALCHEMY_TRACK_CHANGES'] = False

db = SQLAlchemy(app)

# Sample routes to demonstrate template rendering
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    success = False
    
    if request.method == 'POST':
        # Handle login logic here
        email = request.form.get('email')
        password = request.form.get('password')
        
        # For demonstration purposes
        if email == 'demo@example.com' and password == 'password':
            session['user'] = {'name': 'Demo User', 'type': 'buyer'}
            return redirect(url_for('dashboard'))
        else:
            message = 'Invalid email or password'
    
    return render_template('login.html', message=message, success=success)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    success = False
    
    if request.method == 'POST':
        # Handle registration logic here
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        user_type = request.form.get('user_type')
        
        # For demonstration purposes
        message = f'Account created for {name} as {user_type}'
        success = True
    
    return render_template('register.html', message=message, success=success)

@app.route('/products')
def products():
    # Sample product data
    products = [
        {
            'id': 1,
            'name': 'Laptop',
            'price': 999.99,
            'description': 'High-performance laptop with 16GB RAM',
            'stock': 10,
            'image_url': '/static/images/placeholder.jpg'
        },
        {
            'id': 2,
            'name': 'Smartphone',
            'price': 699.99,
            'description': 'Latest smartphone with 128GB storage',
            'stock': 15,
            'image_url': '/static/images/placeholder.jpg'
        },
        {
            'id': 3,
            'name': 'Headphones',
            'price': 149.99,
            'description': 'Noise-cancelling wireless headphones',
            'stock': 0,
            'image_url': '/static/images/placeholder.jpg'
        }
    ]
    
    # Sample categories
    categories = [
        {'id': 1, 'name': 'Electronics'},
        {'id': 2, 'name': 'Clothing'},
        {'id': 3, 'name': 'Home & Kitchen'}
    ]
    
    # Mock pagination
    class Pagination:
        def __init__(self):
            self.page = 1
            self.per_page = 10
            self.total = 3
            self.has_prev = False
            self.has_next = False
            self.prev_num = None
            self.next_num = None
        
        def iter_pages(self):
            return [1]
    
    pagination = Pagination()
    
    return render_template('products.html', 
                          products=products, 
                          categories=categories, 
                          pagination=pagination,
                          selected_category=None,
                          sort='newest')

@app.route('/dashboard')
def dashboard():
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Sample user data
    user = session['user']
    if not isinstance(user, dict):
        user = {'name': 'Demo User', 'type': 'buyer', 'last_login': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    else:
        user['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Placeholder routes for dashboard links
@app.route('/orders')
def orders():
    return "Orders Page"

@app.route('/wishlist')
def wishlist():
    return "Wishlist Page"

@app.route('/manage_listings')
def manage_listings():
    return "Manage Listings Page"

@app.route('/manage_tickets')
def manage_tickets():
    return "Manage Tickets Page"

@app.route('/payment_methods')
def payment_methods():
    return "Payment Methods Page"

@app.route('/sales_analytics')
def sales_analytics():
    return "Sales Analytics Page"

@app.route('/knowledge_base')
def knowledge_base():
    return "Knowledge Base Page"

@app.route('/profile')
def profile():
    return "Profile Page"

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Add to cart logic here
    return redirect(url_for('products'))

@app.route('/buy_now/<int:product_id>')
def buy_now(product_id):
    # Buy now logic here
    return "Buy Now Page"

if __name__ == '__main__':
    app.run(debug=True)
