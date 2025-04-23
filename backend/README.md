# 📚 Bookstore Backend (Django + DRF)

This is the backend API for the Bookstore application, built using **Django** and **Django REST Framework**. It supports user registration, JWT-based authentication, order management, book listings, and role-based access control for buyers, sellers, and admins.

---

## 🚀 Features

- ✅ JWT authentication with access and refresh tokens
- 🛒 Order creation, status updates, and validations
- 📦 Book creation, retrieval, and caching
- 👥 Custom user model with user types: `buyer`, `seller`, `admin`
- 🧠 Global error handling with `custom_exception_handler`
- 🛡️ Role-based permissions and route protection
- 🧹 Book and order data cached for performance (with optional manual invalidation)

---

## 📦 Requirements

- Python 3.10+
- Django 5.x
- djangorestframework
- djangorestframework-simplejwt
- drf-yasg
- SQLite or PostgreSQL

---

## 🛠️ Installation

1. **Clone the project:**
   git clone <https://github.com/erkaracay/bookstore.git>
   cd bookstore/backend

2. **Create a virtual environment:**
   python -m venv .venv
   source .venv/bin/activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **Set up environment (if needed):**
   Update `settings.py` or `.env` for database, secret keys, etc.

5. **Run migrations:**
   python manage.py migrate

6. **Create a superuser:**
   python manage.py createsuperuser

7. **Run the server:**
   python manage.py runserver

---

## 🔐 Authentication

Uses **JWT** via `djangorestframework-simplejwt`.

- `POST /api/token/` – Get access and refresh tokens
- `POST /api/token/refresh/` – Refresh access token
- `POST /api/token/verify/` – Verify token
- `POST /users/logout/` – Invalidate refresh token
- `POST /users/register/` – Register a new user

---

## 👤 User Roles

- `buyer` – Can browse books and place orders
- `seller` – Can add books (must choose `individual` or `company`)
- `admin` – Has full access, including shipping and admin dashboards

---

## 📚 Book API

- `GET /books/` – List all books (cached)
- `POST /books/` – Add new book (admin/seller only)
- `GET /books/<id>/` – Book details
- `GET /books/<slug>/` – Book detail by slug

---

## 📦 Order API

- `GET /orders/` – List user's orders
- `POST /orders/` – Create new order
- `PATCH /orders/<id>/status/` – Update order status (admin only for shipping)
- `POST /orders/<id>/cancel/` – Cancel order

Status transitions:

- `pending` → `shipped` (admin only)
- `pending` → `cancelled`
- Cannot update cancelled/shipped orders

---

## ⚙️ Admin Panel

Superusers can log in to:

- Create admin/seller/buyer accounts
- Manage book listings
- View and manage orders

---

## 🔁 Caching

- `GET /books/` and `GET /books/<id>/` responses are cached for 30 seconds
- You can manually clear caches by calling `cache.clear()` in `django shell`

---

## 🧪 Testing

Tests can be added under the `tests/` directory. Run tests with:
   python manage.py test

---

## 📂 Project Structure

- `books/` – Book model, views, serializers
- `orders/` – Order model, status flow, permissions
- `users/` – Custom user model and registration logic
- `backend/` – Settings, URLs, exception handler
- `exceptions.py` – Custom exception handler for global error messages

---

## ✨ Future Improvements

- Order updates (quantity, items)
- Pagination and filtering
- Email verification and password reset
- Admin dashboard stats
