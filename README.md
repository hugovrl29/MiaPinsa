# MiaPinsa — Online Ordering webapp for an Italian Restaurant in Namur

A full-stack web application built with **Python (Django)** for managing a restaurant menu, orders, and payments.  
Designed to provide customers with a smooth ordering experience while enabling the restaurant to manage products and transactions efficiently.

## ✨ Features
- **Dynamic Menu Management** — add, update, and remove products via Django admin.
- **Shopping Cart** — customers can browse items and add them to their cart before checkout.
- **Secure Payments** — Stripe integration for card transactions (cancelled).
- **Order Tracking** — simple order management flow for the restaurant.

## 🧱 Tech Stack
- **Backend:** Python 3, Django
- **Frontend:** HTML5, CSS3, Bootstrap.js
- **Database:** SQLite (dev)
- **Order Tracking:** Folium, osmnx

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtualenv (recommended)

### Steps
```bash
git clone https://github.com/hugovrl29/MiaPinsa.git
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
