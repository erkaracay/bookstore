# 📚 Bookstore

A full-stack web application for buying and selling books.  
Built with **Django REST** (backend) and **Vue 3 + Vite + Pinia + Tailwind CSS** (frontend).  
Features include JWT auth (buyers & sellers), cart & order management, role-based dashboard, and Dockerized development.

---

## 🚀 Features

- **Home**: Browse all books with title, author, price, and stock alerts  
- **Book Detail**: View full description, adjust quantity, add to cart  
- **Authentication**: Register as Buyer or Seller, Login with JWT  
- **Cart**: Add, update, remove items; checkout with real-time stock updates  
- **Dashboard**:  
  - **Buyer**: View past orders with “time ago” labels  
  - **Seller**: Manage (create/edit/delete) your own books  
  - **Admin**: Redirect to Django Admin panel  
- **Forms**: Real-time validation (Zod), floating labels, custom selects, date-picker  
- **Notifications**: Toasts for add/remove/undo actions  

---

## ⚙️ Prerequisites

- **Python** ≥ 3.11  
- **Node.js** ≥ 18 & npm  
- **Docker** & **Docker Compose** (optional, for containerized dev)

---

## 🏗️ Local Development

### 1. Backend

1. Open a terminal and `cd backend`  
2. Create a virtual environment and activate it:
  
       python3 -m venv .venv
       source .venv/bin/activate
  
3. Install Python dependencies:
  
       pip install -r requirements.txt
  
4. Run migrations & start the server:
  
       python manage.py migrate
       python manage.py runserver 0.0.0.0:8000
  
   The API will be available at `http://localhost:8000/`.

### 2. Frontend

1. In a new terminal, `cd frontend`  
2. Install npm packages:
  
       npm install
  
3. Start Vite’s dev server:
  
       npm run dev
  
   The app will open at `http://localhost:5173/`.

---

## 🐳 Dockerized Development

With Docker & Compose you get live-reload in both services:

1. From the **project root** (next to `docker-compose.yml`):
  
       docker-compose up --build
  
2. Access:
   - **Backend**: `http://localhost:8000/`
   - **Frontend**: `http://localhost:3000/`
  
3. To stop, press `Ctrl+C`, then:
  
       docker-compose down

---

## 🗂️ Project Structure

    .
    ├── backend/              # Django REST API
    │   ├── manage.py
    │   ├── requirements.txt
    │   └── ...
    ├── frontend/             # Vue 3 + Vite + Pinia app
    │   ├── package.json
    │   ├── vite.config.js
    │   ├── src/
    │   └── ...
    ├── docker-compose.yml    # Development orchestration
    └── README.md             # <-- you are here

---

## 🔧 Configuration

- **API Base URL**  
  In `frontend/src/utils/axios.js`, set `baseURL` to match your backend:
  
      http://localhost:8000/
  
- **Environment Variables**  
  If you need secrets or different endpoints, create a `.env` file and reference them via `import.meta.env.VITE_...` in Vite.  

---

## 📄 License

This project is open source under the MIT License.  
Feel free to use, modify, and distribute!
