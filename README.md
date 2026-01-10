# 🧼 Transparent Cleaning Service (TCS) – Backend API

A **RESTful API** for managing a professional cleaning service platform.  
Built with **Django REST Framework**, featuring **JWT authentication**, **cart & order system**, **service catalog**, and **customer reviews**.

---

## 🚀 Features

- 🔐 JWT Authentication (Access & Refresh tokens)
- 👤 User registration, activation, profile management
- 🛒 Cart system with items & total price calculation
- 📦 Order creation, cancellation & status tracking
- 🧹 Service & category management (Admin controlled)
- ⭐ Service reviews & ratings
- 🔎 Filtering, searching & pagination
- 🛡️ Role-based access (Admin / User)
- 📄 Swagger / OpenAPI Documentation

---

## 🛠️ Tech Stack

- Backend: Django, Django REST Framework
- Authentication: JWT (SimpleJWT / Djoser)
- Database: PostgreSQL
- API Docs: Swagger (OpenAPI 2.0)

---

## 🔐 Authentication

### Obtain Token
POST `/api/v1/auth/jwt/create/`

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Use token:
```
Authorization: JWT <access_token>
```

---

## 📌 Main API Endpoints

### Auth
- POST `/auth/jwt/create/`
- POST `/auth/jwt/refresh/`
- GET  `/auth/users/me/`

### Services
- GET `/services/`
- POST `/services/` (Admin)
- GET `/services/{id}/`
- DELETE `/services/{id}/` (Admin)

### Categories
- GET `/categories/`
- POST `/categories/` (Admin)
- UPDATE `/categories/{category_id}` (Admin)
- DELETE `/categories/{category_id}` (Admin)

### Cart
- POST `/carts/`
- POST `/carts/{cart_id}/items/`

### Orders
- POST `/orders/`
- GET `/orders/{id}/`
- POST `/orders/{id}/cancel/`
- PATCH `/orders/{id}/update_status/` (Admin)

### Reviews
- GET `/services/{service_id}/reviews/`
- POST `/services/{service_id}/reviews/`
- GET `/services/{service_id}/reviews/{review_id}`
- POST `/services/{service_id}/reviews/{review_id}`
- DELETE `/services/{service_id}/reviews/{review_id}`

---

## 📖 API Documentation

Swagger UI:
```
http://127.0.0.1:8000/swagger/
```

---


## ⚙️ Installation

```bash
git clone https://github.com/anisul770/TCS.git
cd TCS
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 💳 Future Implementation: Payment Gateway

A payment gateway will be integrated in a future release to support online payments for orders.  
This module will handle secure payment processing, payment status tracking, and order confirmation after successful transactions.

The implementation details (payment methods, providers, and regions) will be finalized later based on business and technical requirements.


---

## 👨‍💻 Author

**Anisul Haque**

---

## 📄 License

MIT License