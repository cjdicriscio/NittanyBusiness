# NittanyBusiness Marketplace

A marketplace platform built with Flask and HTML5/CSS.

## Project Structure

\`\`\`
nittanybusiness/
├── app.py                  # Main Flask application
├── templates/              # HTML templates
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── products.html       # Products listing page
│   └── dashboard.html      # User dashboard
├── static/                 # Static assets
│   ├── css/
│   │   └── styles.css      # Global CSS styles
│   └── images/
│       └── placeholder.jpg # Placeholder image
└── README.md               # Project documentation
\`\`\`

## Setup Instructions

1. Install required packages:
   \`\`\`
   pip install flask flask-sqlalchemy
   \`\`\`

2. Run the application:
   \`\`\`
   python app.py
   \`\`\`

3. Access the application at http://localhost:5000

## Features

- User authentication (login/register)
- Product browsing with filtering and pagination
- Role-based dashboard (Buyer, Seller, HelpDesk)
- Responsive design using Bootstrap

## Integration with Flask

The templates use Jinja2 syntax for integration with Flask:
- Variables: `{{ variable_name }}`
- Control structures: `{% if condition %}...{% endif %}`
- URL generation: `{{ url_for('route_name') }}`

## Notes

This is a frontend template. The backend functionality needs to be implemented.
