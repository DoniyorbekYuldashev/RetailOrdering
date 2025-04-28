Retail Ordering System
A FastAPI-based web application for managing products and orders in a retail environment. The system supports user authentication, admin product management, and customer order creation with a PostgreSQL database.
Table of Contents

Features
Tech Stack
Prerequisites
Installation
Running the Application
API Endpoints
Project Structure
Contributing
License

Features

User Authentication: Sign up, log in, and JWT-based authentication.
Admin Functionality: Add, update, delete, and view products; manage orders; promote users to admin.
Customer Functionality: View products, create orders, and check order status.
Database: PostgreSQL for persistent storage.
Security: Password hashing with bcrypt and JWT for secure authentication.

Tech Stack

Backend: FastAPI (Python)
Database: PostgreSQL
ORM: SQLAlchemy
Authentication: fastapi-jwt-auth, passlib (bcrypt)
Containerization: Docker
Dependencies: Managed via requirements.txt

Prerequisites

Python 3.12+
PostgreSQL
Docker (optional, for containerized deployment)
Git

Installation

Clone the repository:
git clone https://github.com/DoniyorbekYuldashev/retail-ordering.git
cd retail-ordering


Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:
pip install -r requirements.txt


Configure environment variables:Create a .env file in the root directory and add the following:
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=retailOrdering
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60


Set up the PostgreSQL database:

Ensure PostgreSQL is running.
Create a database named retailOrdering.
The application will automatically create the necessary tables on startup.


Running the Application

Run locally with Uvicorn:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


Run with Docker:
docker build -t retail-ordering .
docker run -d -p 8000:8000 --env-file .env retail-ordering


Access the API:

Open http://localhost:8000/docs in your browser for the interactive Swagger UI.


API Endpoints
Authentication (/auth)

POST /signup: Register a new user.
POST /login: Log in and receive JWT tokens.
PUT /users/{id}/make-admin: Promote a user to admin (admin only).

Admin Routes (/admin)

POST /add-product: Create a new product.
GET /get-products: List all products.
GET /get-product/{id}: Get a specific product.
PUT /update-product/{id}: Update a product.
DELETE /delete-product/{id}: Delete a product.
GET /orders: List all orders.
GET /get-order/{id}: Get a specific order.

Customer Routes (/customer)

GET /products: List all products.
POST /make-order: Create a new order.
GET /get-order/{customerId}: List orders for a customer.
GET /get-order/{orderId}/status: Check the status of an order.

Project Structure
retail-ordering/
├── admin/
│   ├── routes.py         # Admin API routes
│   ├── schemas.py       # Pydantic schemas for admin
├── auth/
│   ├── routes.py        # Authentication routes
│   ├── schemas.py       # Pydantic schemas for auth
├── customer/
│   ├── routes.py        # Customer API routes
│   ├── schemas.py       # Pydantic schemas for customer
├── main.py              # FastAPI application entry point
├── config.py            # Configuration settings
├── database.py          # Database setup and session management
├── dependency.py        # Dependency injection
├── models.py            # SQLAlchemy models
├── utils.py             # Utility functions (e.g., password hashing)
├── Dockerfile           # Docker configuration
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation

Contributing

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request."# RetailOrdering" 
