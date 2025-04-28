# NittanyBusiness Marketplace

A marketplace platform built with Flask and HTML5/CSS.

## Project Structure

NittanyBusiness/ <br>
├── NittanyBusinessDataset/ <br>
├── static/ <br>
│   ├── css/<br>
│   │   └── styles.css<br>
│   └── images/<br>
├── templates/<br>
│   ├── cart.html # Shopping cart<br>
│   ├── checkout.html # Where the user can pay for their cart<br>
│   ├── createProductListing.html # Where the seller makes a new listing<br>
│   ├── dashboard.html # homepage<br>
│   ├── deleteProductListing.html # Where the seller removes listings<br>
│   ├── editProductListing.html # Where the seller edits an exisitng listing<br>
│   ├── leave_review.html # where reviews can be made<br>
│   ├── login.html # First page where users login<br>
│   ├── manage_helpdesk_accounts.html # where helpdesk accounts are denied or accepted<br>
│   ├── manage_requests.html # Where helpdesk employees work on tickets<br>
│   ├── navbar.html<br>
│   ├── orders.html # Shows user orders<br>
│   ├── payment_methods.html<br>
│   ├── product_info.html<br>
│   ├── productListings.html<br>
│   ├── products.html # Grid of organized products for sale<br>
│   ├── profile.html # User profile for changing attributes<br>
│   ├── register.html # First register page<br>
│   ├── registerBuyer.html # Where buyers finish registering<br>
│   ├── registerHelpDesk.html # Where help desk employees finish registering<br>
│   ├── registerSeller.html # Where sellers finish registering<br>
│   ├── seller_reviews.html # Where users can review sellers<br>
│   ├── submit_request.html # Where users can submit a request for the helpdesk to fix<br>
│   ├── thank_you.html<br>
│   └── update_request.html # Updates user request<br>
├── app.py                  # Flask file with routes<br>
├── checking.ipynb<br>
├── initialize_db.py        # Initializes database with given data<br>
├── README.md               # You are here<br>
├── requirements.txt        # Python package dependencies<br>
├── .gitignore<br>
└── database.db             # SQLite database with all tables<br>


## Data Structure

SQLite was used to manage data for this project.

### Tables
PK := primary key <br>
FK := foreign key
#### Users
- `email`: User's email (PK)
- `password`: User's password

#### Helpdesk
- `email`: Helpdesk staff's email (Primary Key)
- `position`: Position of the helpdesk staff

#### Requests
- `request_id`: Unique identifier for the request (PK)
- `sender_email`: Email of the user sending the request (FK to `Users`)
- `helpdesk_staff_email`: Email of the helpdesk staff working on the request (FK to `Helpdesk`)
- `request_type`: Type of request
- `request_desc`: Description of the request
- `request_status`: Status of the request (0: Incomplete, 1: Completed)

#### Buyer
- `email`: Email of the buyer (PK, FK `Users`)
- `business_name`: Business name of the buyer
- `buyer_address_id`: Address ID for the buyer (FK to `Address`)

#### Credit_Cards
- `credit_card_num`: Credit card number (PK)
- `card_type`: Type of credit card (company: AMEX, MasterCard, Visa)
- `expire_month`: Expiration month of the credit card
- `expire_year`: Expiration year of the credit card
- `security_code`: Security code on back of the credit card
- `Owner_email`: Email of the credit card owner (FK to `Buyer`)

#### Address
- `address_ID`: Unique identifier for the address (PK)
- `zipcode`: Zipcode of the address (FK to `Zipcode_Info`)
- `street_num`: Street number of the address
- `street_name`: Street name of the address

#### Zipcode_Info
- `zipcode`: Zipcode (PK)
- `city`: City of the zipcode area
- `state`: State of the zipcode area

#### Sellers
- `email`: Email of the seller (PK, FK to `Users`)
- `business_name`: Name of the seller's business
- `business_address_id`: Address ID for the seller's business (FK to `Address`)
- `bank_routing_number`: Seller's bank routing number
- `bank_account_number`: Seller's bank account number
- `balance`: Seller's total balance on the platform

#### Categories
- `parent_category`: Parent category of the current category (FK to `Categories`)
- `category_name`: Name of the category

#### Product_Listings
- `Seller_Email`: Email of the seller (PK, FK to `Sellers`)
- `Listing_ID`: Unique listing identifier (PK)
- `Category`: Category of the product (FK to `Categories`)
- `Product_Title`: Title of the product
- `Product_Name`: Display name of the product
- `Product_Description`: Description of the product
- `Quantity`: Available quantity of the product
- `Product_Price`: Price of one unit of product
- `Status`: Status of the product listing (0: Inactive, 1: Active, 2: Sold out)

### Orders
- `Order_ID`: Unique identifier for the order (PK)
- `Seller_Email`: Email of the seller (FK to `Sellers`)
- `Listing_ID`: Listing identifier of the product ordered (FK to `Product_Listings`)
- `Buyer_Email`: Email of the buyer (FK to `Buyer`)
- `Date`: Date when the order was placed
- `Quantity`: Number of products ordered
- `Payment`: Total payment amount for the order

### Reviews
- `Order_ID`: Unique identifier for the order (FK to `Orders`)
- `Review_Desc`: Description of the review
- `Rating`: Rating given for the product (1 to 5 stars)


## Setup Instructions

1. Install required packages in same directory: <br>
   pip install -r requirements.txt

2. Run the database intializer: <br>
   python initialize_db.py

2. Run the application:<br>
   python app.py

3. Access the application at http://localhost:5000

## Features

- User authentication (login/register)
- Product browsing with filtering by category and direct search
- Role-based dashboard (Buyer, Seller, HelpDesk)
- Leave and read product and seller reviews
- Ability to update user profile
- Product order management for buyers
- Product listing management for sellers
- Responsive design using Bootstrap

## Extra Credit Features

- Shopping Cart
- HelpDesk Support for adding categories

### Citations (Resources used for each technology)
- SQLite: https://www.sqlitetutorial.net/
- Flask: https://flask.palletsprojects.com/en/stable/tutorial/
- Python: https://docs.python.org/3/tutorial/index.html 
- Bootstrap: https://getbootstrap.com/docs/4.1/getting-started/introduction/
- HTML: https://developer.mozilla.org/en-US/docs/Web/HTML
- CSS: https://developer.mozilla.org/en-US/docs/Web/CSS
- Penn State Lectures and Material for CMPSC 431W provided by Wang-Chien Lee and associates
