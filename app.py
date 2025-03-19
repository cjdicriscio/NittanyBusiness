from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql
import csv
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session key

DATABASE = 'database.db'
CSV_FILE = 'Users.csv'  # Ensure Users.csv is in the same directory


# -------------------------------
# 🔹 Database Utility Functions
# -------------------------------

def create_user_table():
    """Create the users table if it does not exist."""
    print("Debug: Creating users table if not exists...")
    with sql.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        connection.commit()
    print("Debug: Users table ready!")


def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def populate_users():
    """Load users from CSV and insert into the database with hashed passwords."""
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: {CSV_FILE} not found!")
        return

    print("🔄 Debug: Opening database connection for inserting users...")
    with sql.connect(DATABASE) as connection:
        cursor = connection.cursor()
        print("🔄 Debug: Reading Users.csv...")

        try:
            with open(CSV_FILE, newline='', encoding='utf-8-sig') as file:
                reader = csv.reader(file)  # Read as plain rows to debug

                # Print every row from the file
                for i, row in enumerate(reader):
                    print(f"🔍 Debug: Row {i} -> {row}")

                # Reset file pointer and read with DictReader
                file.seek(0)
                reader = csv.DictReader(file)

                users = []
                for row in reader:
                    email = row.get('email', '').strip()
                    password = row.get('password', '').strip()

                    if email and password:
                        hashed_password = hash_password(password)
                        users.append((email, hashed_password))
                        print(f"✅ Debug: Queued for insertion -> Email: {email}")

                if users:
                    cursor.executemany('INSERT OR IGNORE INTO users (email, password) VALUES (?, ?);', users)
                    print(f"✅ Debug: Inserted {len(users)} users into the database!")
                else:
                    print("⚠️ Debug: No valid users found in CSV!")

            connection.commit()
        except Exception as e:
            print(f"❌ Error reading Users.csv: {e}")

    print("✅ Debug: Database population complete!")



def get_all_users():
    """Retrieve all users from the database for debugging."""
    print("🔍 Debug: Fetching all users from database...")
    with sql.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT email, password FROM users;")
        users = cursor.fetchall()
        print(f"✅ Debug: Retrieved {len(users)} users from database.")
        for user in users:
            print(f"📌 Debug: User -> {user[0]} | Hashed Password -> {user[1]}")
        return users


def count_users():
    """Returns the number of users in the database."""
    print("🔍 Debug: Counting users in database...")
    with sql.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        count = cursor.fetchone()[0]
    print(f"✅ Debug: Total Users in DB -> {count}")
    return count


def get_user(email, hashed_password):
    """Retrieve a user from the database by email and hashed password."""
    print(f"🔍 Debug: Checking login for {email}")
    with sql.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?;', (email, hashed_password))
        user = cursor.fetchone()
    if user:
        print(f"✅ Debug: User {email} found in DB!")
    else:
        print(f"❌ Debug: User {email} not found or incorrect password.")
    return user


# -------------------------------
# 🔹 Flask Routes
# -------------------------------

@app.route('/')
def index():
    """Redirect to the login page."""
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Authenticate users using email and password."""
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)  # Hash input password

        print(f"🔍 Debug: Hashed input password -> {hashed_password}")

        user = get_user(email, hashed_password)  # Fetch user from DB
        if user:
            session['user'] = email  # Store user session
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid email or password.'

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    """Protected route that requires login."""
    if 'user' in session:
        return f"✅ Welcome {session['user']}! You are logged in."
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """Logout user and clear session."""
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    # Delete old database to ensure proper password hashing
    if os.path.exists(DATABASE):
        print("🔄 Debug: Deleting old database to start fresh...")
        os.remove(DATABASE)

    create_user_table()
    populate_users()
    count_users()  # Debug: Show total users
    get_all_users()  # Debug: Show all users

    print("🚀 Debug: Flask app is starting now...")
    app.run(debug=True)
