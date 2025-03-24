# NittanyBusiness

## Overview

Nittany Business is an online ecommerce application built with Flask and SQLite. It maintains and manages operations performed by sellers, buyers, product listings, help desk employess, reviews, and orders.

## Project Structure

|=NITTANYBUSINESS  
|  
|==NittanyBusinessDataset  
|---📄Address.csv  
|---📄Buyers.csv  
|---📄Categories.csv  
|---📄Credit_Cards.csv  
|---📄Helpdesk.csv  
|---📄Orders.csv  
|---📄Product_Listings.csv  
|---📄Requests.csv  
|---📄Reviews.csv  
|---📄Sellers.csv  
|---📄Users.csv  
|---📄Zipcode_Info.csv  
|  
|==templates  
|---📝index.html  
|---📝input.html  
|---📝login.html  
|  
|--🐍app.py  
|--🗃️database.db  
|--📑README.md  

## Setup

1. Install Dependencies  

Open terminal and type install with "pip install flask sqlite3"

2. Run app.py

Open app.py and click the "Run" arrow at the top right of VSCode or PyCharm. Alternatively, you can type "python app.py" to run.

3. Navigate to the website

Copy and paste http://127.0.0.1:5000 into your preferred browser after the Flask app is running. Press enter. This will take you to the login page.

4. Enter in valid credentials

Type desired email and password in respective fields. Click the blue "Login" button below to navigate into the app.