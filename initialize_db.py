import sqlite3 as sql
import csv
import hashlib
import os

DATABASE = 'database.db'
PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(PARENT_DIR, "NittanyBusinessDataset", "Users.csv")

#------------------------------------------------------------------------------
# Create Tables with Associated Attributes
#------------------------------------------------------------------------------

# Users Table
def create_user_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
    ''')
    connection.commit()
    connection.close()

# HelpDesk Table
def create_helpdesk_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Helpdesk (
            email TEXT PRIMARY KEY,
            position TEXT NOT NULL
        );
    ''')
    connection.commit()
    connection.close()

# Requests Table
def create_requests_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_email TEXT NOT NULL
            helpdesk_staff_email TEXT NOT NULL
            request_type TEXT NOT NULL
            request_desc TEXT NOT NULL
            request_status INTEGER NOT NULL
        );
    ''')
    connection.commit()
    connection.close()

# Buyers Table
def create_buyers_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Buyers (
            email TEXT PRIMARY KEY,
            business_name TEXT NOT NULL
            buyer_address_id TEXT NOT NULL
            FOREIGN KEY email REFERENCES Users email
            FOREIGN KEY buyer_address_id REFERENCES Address address_id
        );
    ''')
    connection.commit()
    connection.close()

# CreditCard Table
def create_creditcard_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CreditCards (
            credit_card_num INTEGER PRIMARY KEY,
            card_type TEXT NOT NULL
            expire_month TEXT NOT NULL
            expire_year TEXT NOT NULL
            security_code INTEGER NOT NULL
            owner_email TEXT NOT NULL
            FOREIGN KEY owner_email REFERENCES Users email
        );
    ''')
    connection.commit()
    connection.close()

# Address Table
def create_address_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Address (
            address_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zipcode INTEGER NOT NULL
            street_num INTEGER NOT NULL
            street_name TEXT NOT NULL
            FOREIGN KEY owner_email REFERENCES Users email
        );
    ''')
    connection.commit()
    connection.close()

# Zipcode Table
def create_zipcode_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Zipcode (
            zipcode INTEGER PRIMARY KEY,
            city TEXT NOT NULL
            state TEXT NOT NULL
        );
    ''')
    connection.commit()
    connection.close()

# Sellers Table
def create_sellers_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sellers (
            email TEXT PRIMARY KEY,
            business_name TEXT NOT NULL
            business_address_id TEXT NOT NULL
            bank_routing_num INTEGER NOT NULL
            bank_acct_num INTEGER NOT NULL
            balance INTEGER NOT NULL
            FOREIGN KEY email REFERENCES Users email
            FOREIGN KEY business_address_id REFERENCES Address address_id
        );
    ''')
    connection.commit()
    connection.close()
    
# Categories Table
def create_categories_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            cat_name TEXT PRIMARY KEY
            parent_cat TEXT
            FOREIGN KEY parent_cat REFERENCES Categories cat_name
        );
    ''')
    connection.commit()
    connection.close()

# ProductLists Table
def create_productlistings_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ProductListings (
            seller_email TEXT PRIMARY KEY
            listing_id INTEGER PRIMARY KEY AUTOINCREMENT
            category TEXT NOT NULL
            product_name TEXT NOT NULL
            product_desc TEXT NOT NULL
            quantity INTEGER NOT NULL
            product_price INTEGER NOT NULL
            status INTEGER NOT NULL
            FOREIGN KEY seller_email REFERENCES Users email
            FOREIGN KEY category REFERENCES Categories cat_name
        );
    ''')
    connection.commit()
    connection.close()

# Orders Table
def create_orders_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT
            seller_email TEXT NOT NULL
            buyer_email TEXT NOT NULL
            listing_id INTEGER NOT NULL
            date DATETIME NOT NULL
            quantity INTEGER NOT NULL
            payment INTEGER NOT NULL
            FOREIGN KEY seller_email REFERENCES Sellers email
            FOREIGN KEY buyer_email REFERENCES Buyers email
            FOREIGN KEY listing_id REFERENCES ProductListings listing_id
        );
    ''')
    connection.commit()
    connection.close()

# Reviews Table
def create_orders_table():
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reviews (
            order_id INTEGER PRIMARY KEY
            review_desc TEXT
            rating INTEGER NOT NULL
            FOREIGN KEY order_id REFERENCES Orders order_id
        );
    ''')
    connection.commit()
    connection.close()

#------------------------------------------------------------------------------
# Populate Tables
#------------------------------------------------------------------------------

def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def populate_users():
    """Load users from CSV and insert into the database with hashed passwords."""
    connection = sql.connect(DATABASE)
    cursor = connection.cursor()

    # Read CSV and populate users table
    with open(CSV_FILE, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row.get('\ufeffemail', '').strip()
            password = row.get('password', '').strip()
            hashed_password = hash_password(password)  # Hash it before storing

            if email and password:  # Ensure values exist
                try:
                    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?);', (email, hashed_password))
                except sql.IntegrityError:
                    pass  # Skip duplicate emails

    connection.commit()
    connection.close()




if __name__ == "__main__":
    # Delete old database to ensure proper password hashing
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    create_user_table()
    populate_users()
    app.run(debug=True)
