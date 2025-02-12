E-Commerce Backend Website 🛒

Overview

This is a fully functional backend for an e-commerce website, built using Python and Django. The project provides essential e-commerce features like user authentication, add-to-cart functionality, and payment gateway integration. It follows Django’s MVT (Model-View-Template) architecture and ensures secure and efficient database management using Django ORM.

Features

✅ User Authentication – Signup, login, logout with secure password hashing and email verification.
✅ Product Management – Retrieve product listings from the database using Django ORM.
✅ Cart System – Add, update, and remove products from the shopping cart.
✅ Order Management – Store user orders and manage transactions.
✅ Payment Gateway Integration – Simulated payment process for checkout.
✅ Security – CSRF protection, secure authentication, and data validation.

Tech Stack

Backend: Django (Python)
Database: SQLite (can be switched to PostgreSQL or MySQL)
Authentication: Django’s built-in authentication system with email verification
Version Control: Git & GitHub

Installation & Setup
1.Clone the Repository
git clone https://github.com/JyotiMofficial/ecomm-website.git
cd ecomm-website

2.Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows

3.Install Dependencies
pip install -r requirements.txt
4.Run Migrations
python manage.py migrate

5.Start the Development Server
python manage.py runserver


Future Enhancements

🔹 Add product search and filtering options
🔹 Implement a real payment gateway (e.g., Razorpay, Stripe)
🔹 Improve UI with a frontend framework like React

