# MySushi – Web Ordering App

## Description
A web application for ordering food online. The system allows users to browse products, add them to a cart, and manage orders.

## Tech Stack
- **Backend:** Django
- **Database:** PostgreSQL
- **Frontend:** Bootstrap
- **Testing:** Pytest

## Features
- Session-based shopping cart
- Add, remove, and update cart items
- Order management system
- CRUD operations for products and orders
- Relational database structure
- Basic automated tests

## Application Flow
- User browses products
- Adds items to cart
- Updates cart (add/remove/change quantity)
- Proceeds to order

## How to Run

```bash
git clone https://github.com/Jopus7/MySushi-
cd MySushi-
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
