from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3 as sql
import os
import hashlib
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nittanybusiness.db'
app.config['SQLALCHEMY_TRACK_CHANGES'] = False

db = SQLAlchemy(app)

Data = os.path.join(os.path.dirname(__file__), 'database.db')

DATABASE = 'database.db'

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# Sample routes to demonstrate template rendering
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message, success = None, False

    flashed = get_flashed_messages()
    if flashed:
        try:
            message, success = flashed[0]
        except ValueError:
            message = flashed[0]
            success = None
    
    if request.method == 'POST':
        # Handle login logic here
        email = request.form.get('email')
        password = request.form.get('password')
        
        
        #demo credentials if no Database, remove in full ver.
        if email == 'demo@example.com' and password == 'password':
            session['user'] = {'id': 'email', 'name': 'userName', 'type': 'userType'}
            return redirect(url_for('dashboard'))
        
        hashed_password = hash_password(password)

        try:
            connection = sql.connect(DATABASE)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?;', (email, hashed_password))
            user = cursor.fetchone()
            connection.commit()
            
            if user:
                email = user[0]
                userName = ""
                
                # checks buyer table to see if user is a buyer
                cursor.execute('SELECT business_name FROM Buyers WHERE email = ?;', (email,))
                buyerResult = cursor.fetchone()
                isBuyer = buyerResult is not None
                connection.commit()
                
                # checks sellers table to see if user is a buyer
                cursor.execute('SELECT Business_name FROM Sellers WHERE email = ?;', (email,))
                sellerResult = cursor.fetchone()
                isSeller = sellerResult is not None
                connection.commit()
                
                if isBuyer:
                    userName = buyerResult[0]
                    userType = 'Buyer'
                elif isSeller:
                    userName = sellerResult[0]
                    userType = 'Seller'
                else:
                    userName = email
                    userType = 'Help Desk'
                
                #update session to include logged in user
                session['user'] = {'id': email, 'name': userName, 'type': userType}
                
        except Exception as e:
            print(e)
        finally:
            if connection:
                connection.close() 
        

        if user:
            return redirect(url_for('dashboard'))
        else:
            message = 'Invalid email or password.'
    
    return render_template('login.html', message=message, success=success)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        #email = request.form.get('email')
        #password = request.form.get('password')
        #confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type')
        session['userRegistration'] = {
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'name': request.form.get('name'),
        }

        # redirect to second registration page based on user type
        if user_type == 'buyer':
            return redirect(url_for('registerBuyer'))
        elif user_type == 'seller':
            return redirect(url_for('registerSeller'))
        elif user_type == 'helpdesk':
            return redirect(url_for('registerHelpDesk'))
        
    return render_template('register.html')

@app.route('/registerBuyer', methods=['GET', 'POST'])
def registerBuyer():
    message, success = "", False
    
    if request.method == 'POST':
        userRegistration = session.get('userRegistration', {})
        # goes into User table
        email = userRegistration.get('email')
        password = userRegistration.get('password')
        password = hash_password(password)
        
        # goes into Buyers table
        business_name = request.form.get('name')
        
        # goes into Address Table
        zipcode = request.form.get('zipcode')
        street_num = request.form.get('street_num')
        street_name = request.form.get('street_name')
        
        # connects Buyers and Address
        address_id = uuid.uuid4().hex
        
        # Add validation and database operations
        try:
            # Add the buyer to database
            connection = sql.connect(DATABASE)
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO Users(email,password)
                VALUES(?,?)
            ''', (email, password))
            connection.commit()
            cursor.execute('''
                INSERT INTO Buyers(email,business_name,buyer_address_id)
                VALUES(?,?,?)
            ''', (email, business_name,address_id))
            connection.commit()
            cursor.execute('''
                INSERT INTO Address(address_ID,zipcode,street_num,street_name)
                VALUES(?,?,?,?)
            ''', (address_id, zipcode, street_num, street_name))
            connection.commit()
            
            message = f'Buyer account created for {business_name}'
            success = True
            flash((message, success))
            
            return redirect(url_for('login'))
        except Exception as e:
            message = f'Failed to create account: {e}'
            success = False
        finally:
            if connection:
                connection.close()

    return render_template('registerBuyer.html', message=message, success=success)


@app.route('/registerHelpDesk', methods=['GET', 'POST'])
def registerHelpDesk():
    message, success = "", False
    
    if request.method == 'POST':
        userRegistration = session.get('userRegistration', {})
        #print(userRegistration)
        email = userRegistration.get('email')
        password = userRegistration.get('password')
        password = hash_password(password)
        position = request.form.get('position')
        
        # Add validation and database operations
        try:
            # Add the helpdesk to database
            connection = sql.connect(DATABASE)
            cursor = connection.cursor()
            cursor = cursor.execute('''
                INSERT INTO Users(email,password)
                VALUES(?,?)
            ''', (email, password))
            connection.commit()
            cursor = cursor.execute('''
                INSERT INTO Helpdesk(email,position)
                VALUES(?,?)
            ''', (email, position))
            connection.commit()
            connection.close()
            
            message = f'Help Desk account created successfully!'
            success = True
            flash((message, success))
            
            return redirect(url_for('login'))
        except Exception as e:
            message = f'Failed to create account: {e}'
            success = False
        finally:
            if connection:
                connection.close()

    return render_template('registerHelpDesk.html', message=message, success=success)


@app.route('/registerSeller', methods=['GET', 'POST'])
def registerSeller():
    if request.method == 'POST':
        userRegistration = session.get('userRegistration', {})
        
        # for Users table
        email = userRegistration.get('email')
        password = userRegistration.get('password')
        password = hash_password(password)
        
        # for Sellers table
        Business_Name = request.form.get('Business_Name')
        address_id = uuid.uuid4().hex
        bank_routing_number = request.form.get('bank_routing_number')
        bank_account_number = request.form.get('bank_account_number')
        balance = 0 #default
        
        # goes into Address Table
        zipcode = request.form.get('zipcode')
        street_num = request.form.get('street_num')
        street_name = request.form.get('street_name')
        
        # Add validation and database operations
        try:
            # Add the seller to database
            connection = sql.connect(DATABASE)
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO Users(email,password)
                VALUES(?,?)
            ''', (email, password))
            connection.commit()
            cursor.execute('''
                INSERT INTO Sellers(email, Business_Name, Business_Address_Id, bank_routing_number,bank_account_number, balance)
                VALUES(?,?,?,?,?,?)
            ''', (email, Business_Name, address_id, bank_routing_number,bank_account_number, balance))
            connection.commit()
            cursor.execute('''
                INSERT INTO Address(address_ID,zipcode,street_num,street_name)
                VALUES(?,?,?,?)
            ''', (address_id, zipcode, street_num, street_name))
            connection.commit()
            connection.close()
            
            message = f'Seller account created successfully!'
            success = True
            flash((message, success))
            
            return redirect(url_for('login'))
        except Exception as e:
            message = f'Failed to create account: {e}'
            success = False
        finally:
            if connection:
                connection.close()

    return render_template('registerSeller.html', message=message, success=success)


@app.route('/products')
def products():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()

    selected_category = request.args.get('category')

    # Recursively find all products under the current category
    if (selected_category):
        cursor.execute(f'''
        WITH RECURSIVE subcategories(category_name) AS (
            SELECT category_name
            FROM Categories
            WHERE category_name = ?

            UNION ALL

            SELECT c.category_name
            FROM Categories c
            INNER JOIN subcategories s ON c.parent_category = s.category_name
        )
        SELECT * FROM ProductListings
        WHERE category IN (SELECT category_name FROM subcategories)
        ''', (selected_category,))

    # Initially display all products before filtering
    else:
        cursor.execute('''SELECT * FROM ProductListings''')

    # Preprocess the products into a better format for HTML
    attributes = ['sellerEmail', 'id', 'category', 'title', 'name', 'description', 'quantity', 'price', 'status']
    products = [dict(zip(attributes, row)) for row in cursor.fetchall()]


    # Find subcategories one level below current category
    if (selected_category):
        cursor.execute('''
            SELECT (category_name) 
            FROM Categories
            WHERE parent_category=?
                       
            UNION
                       
            SELECT (category_name)
            FROM Categories
            WHERE category_name=?         
            ''', (selected_category,selected_category))
    
    # Default Categories
    else:
        cursor.execute('''SELECT (category_name) 
            FROM Categories 
            WHERE parent_category = ?''', ("Root",))
    
    # Preprocessing into a string
    categories = [row[0] for row in cursor.fetchall()]

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
    print(selected_category)
    return render_template('products.html', 
                          products=products,
                          categories=categories,
                          pagination=pagination,
                          selected_category = selected_category
                          )

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

@app.route('/update_request/<int:request_id>', methods=['GET', 'POST'])
def update_request(request_id):
    if 'user' not in session:
        flash('You must be logged in to access your profile.', 'error')
        return redirect(url_for('login'))
    
    elif session['user']['type'] != 'Help Desk':
        flash('You must be Help Desk to access this page.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        new_category = request.form.get('new_category')
        parent_category = request.form.get('parent_category')
        new_sender_email = request.form.get('new_sender_email')
        new_request_status = request.form.get('new_request_status')

        try:
            connection = sql.connect(DATABASE)
            cursor = connection.cursor()
            if new_category:
                cursor.execute("""
                    INSERT INTO Categories(category_name,parent_category)
                    VALUES(?,?)
                """, (new_category, parent_category))
                connection.commit()

            if new_sender_email:
                cursor.execute('SELECT * FROM Requests WHERE request_id = ?;', (request_id,))
                req = cursor.fetchone()
                sender_email = req[1]
                cursor.execute("""
                    UPDATE Users
                    SET email = ?
                    WHERE email = ?
                """, (new_sender_email, sender_email))
                connection.commit()

            if new_request_status is not None:
                cursor.execute("""
                    UPDATE Requests
                    SET request_status = ?
                    WHERE request_id = ?
                """, (int(new_request_status), request_id))
                connection.commit()
            
        except Exception as e:
            print(e)
        finally:
            if connection:
                connection.close() 
        return redirect(url_for('manage_requests'))

    return render_template('update_request.html', request_id=request_id)

@app.route('/manage_requests')
def manage_requests():
    if 'user' not in session:
        flash('You must be logged in to access your profile.', 'error')
        return redirect(url_for('login'))
    
    elif session['user']['type'] != 'Help Desk':
        flash('You must be Help Desk to access this page.', 'error')
        return redirect(url_for('dashboard'))
    
    try:
        connection = sql.connect(DATABASE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Requests WHERE request_status = 0")
        requests_list = cursor.fetchall()
        requests = []
        for i,x in enumerate(requests_list):
            requests.append({})
            requests[i]['request_id'] = x[0]
            requests[i]['sender_email'] = x[1]
            requests[i]['helpdesk_email'] = x[2]
            requests[i]['request_type'] = x[3]
            requests[i]['request_desc'] = x[4]
            requests[i]['request_status'] = x[5]
        connection.commit()
            
    except Exception as e:
        print(e)
    finally:
        if connection:
            connection.close() 

    return render_template('manage_requests.html', requests=requests)

@app.route('/payment_methods')
def payment_methods():
    return "Payment Methods Page"

@app.route('/sales_analytics')
def sales_analytics():
    return "Sales Analytics Page"

@app.route('/knowledge_base')
def knowledge_base():
    return "Knowledge Base Page"

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        flash('You must be logged in to access your profile.', 'error')
        return redirect(url_for('login'))
    user = session['user']

    if request.method == 'POST':
        
        passcode = request.form.get('passcode')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        hashed_password = hash_password(passcode)

        user = session['user']
        email = user['id']
        if new_password != confirm_password:
            
            flash('Passwords do not match.', 'error')
            return redirect(url_for('profile'))
        
        try:
            #print('good')
            connection = sql.connect(DATABASE)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?;', (email, hashed_password))
            user = cursor.fetchone()
            connection.commit()
            #print('good')
            if user:
                new_hashed_password = hash_password(new_password)
                #print('good')
                cursor.execute("""
                    UPDATE users
                    SET password = ?
                    WHERE email = ?
                """, (new_hashed_password, email))
                connection.commit()
                #print('good')
                #flash('Password updated successfully!', 'success')
            else:
                #print('inv')
                flash('Invalid passcode.', 'error')
                return redirect(url_for('profile'))
            
        except Exception as e:
            #print('good')
            print(e)
        finally:
            if connection:
                connection.close() 
        
    return render_template('profile.html', user=user)

@app.route('/submit_request', methods=['GET', 'POST'])
def submit_request():
    if 'user' not in session:
        flash('You must be logged in to access your profile.', 'error')
        return redirect(url_for('login'))
    user = session['user']
    if request.method == 'POST':
        request_type = request.form.get('request_type')
        description = request.form.get('description')

        helpdesk_email = 'helpdeskteam@nittybiz.com'
        request_status = 0
        email = user['id']
        if not request_type or not description:
            flash('All fields are required.', 'error')
            return redirect(url_for('submit_request'))
        try:
            #print('good')
            connection = sql.connect(DATABASE)
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Requests (sender_email, helpdesk_staff_email, request_type, request_desc, request_status)
            VALUES (?, ?, ?, ?, ?)""", (email, helpdesk_email, request_type, description, request_status))
            connection.commit()
            #print('good')
            flash('Helpdesk request submitted successfully!', 'success')
            
        except Exception as e:
            #print('good')
            print(e)
        finally:
            if connection:
                connection.close()

    return render_template('submit_request.html')

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
