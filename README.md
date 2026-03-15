
# Django Real-Time Chat Application
A modern Real-Time Chat Application built with Django.

Users can register, login, join chat rooms, and send messages in real-time using WebSockets.
This project is built step-by-step to learn Django Backend Development, Real-time Communication, and REST API development.

---

# 🚀 Project Goal 
The goal of this project is to learn and implement.
- Django Backend Development 
- Real-time Chat using WebSockets 
- Django Channels 
- Chat Room System
- Authentication System
- Message CRUD System
- Online/Offline User Status
- PostgreSQL Database Integration 
- Django REST Framework APIs 
- JWT Authentication 
- Deployment 

---

# 📌 Tech Stack 

Backend:
- Python 
- Django
- Django Channels 
- Django REST Framework 
- JWT Authentication(SimpleJWT)

Database:
- SQLite(Development)
- PostgreSQL(Production)

Frontend:
- HTML
- TailwindCSS
- JavaScript
- WebSocket API

Tools:
- Git
- GitHub
- VS Code
- Postman

Deployment:
-Render

---

# 📂 Project Structure
```text
chat-app/
│
├── core/                       # Django project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                   # Authentication system
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── chat/                       # Chat application
│   ├── migrations/
│   │
│   ├── templates/
│   │   └── chat/
│   │       └── chat_room.html
│   │
│   ├── models.py
│   ├── consumers.py
│   ├── routing.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
│
├── templates/                 # Global templates
│   ├── base.html
│   │
│   └── registration/
│        ├── login.html
│        └── signup.html
│
├── static/
│   ├── css/
│   │   └── output.css
│   └── js/
│       └── chat.js
│
├── tailwind.config.js
├── package.json
│
├── .env
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Environment Setup
- Clone Repository
git clone https://github.com/mamun-2025/real-time-chat-app
cd Django-Chat-App

- Create Virtual Environment:
python -m venv venv

- Activate Virtual Environment:
Windows: venv\Scripts\activate

Install Dependencies:
pip install -r requirements.txt

- Run Migrations:
python manage.py makemigrations
python manage.py migrate

- Run Server:
python manage.py runserver

---

# 🎯 Development Progress

✅ Step 1: Project Setup
Completed:

- Python Installed
- Django Installed
- Django Project Created
- Chat App Created
- Development Server Running

Commands
```bash
pip install django
django-admin startproject core
cd core
python manage.py startapp chat
python manage.py migrate
python manage.py runserver

Status: ✅ Completed

# ⏳ Step 2: Authentication System & TailwindCSS

Implemented Features:
- User Signup
- User Login
- User Logout
- TailwindCSS Setup
- Templates(base.html, login.html, signup.html)

Status: ✅ Completed
```
---

# ⏳ Step 3: Chat Models

Implemented Features:
- Chat Room Model
- Message Model
- User Message Relationship
- Message Timestamp

Example Models:
- Room
- Message

Status: ⏳ In Progress

# ⏳ Step 4: Chat UI

Implemented Features:
- Chat Interface
- Message Input Box
- Send Message Button
- Chat Window Layout

Status: ⏳ Planned

# ⏳ Step 5: Real-Time Chat (WebSocket)

Implemented Features:
- Django Channels setup
- WebSocket Connection
- Real-time Message Sending
- Real-time Message Receiving

Main Files:
- consumers.py
- routing.py
- asgi.py

Status: ⏳ Planned

# ⏳ Step 6: Chat API (DRF)

Implemented Features:
- Message API
- Room API
- User-based message filtering
- JWT Authentication

Example APIs:
- GET /api/messages/
- POST /api/messages/
- GET /api/rooms/

Status: ⏳ Planned

# ⏳ Step 7: Online / Offline Status

Implemented Features:
- Track active users
- Online / Offline status
- Last seen feature

Status: ⏳ Planned

# ⏳ Step 8: Database Upgrade

Planned Features:
- PostgreSQL Integration
- Environment Variables (.env)

Status: ⏳ Planned

# ⏳ Step 9: Deployment (Render)

Deployment Steps:
- GitHub Repository Push
- Environment Variables Setup
- PostgreSQL Database
- Render Deployment

Status: ⏳ Planned

---

# ⭐ Future Improvements

- Planned Features:
- Typing Indicator
- Message Seen Status
- Group Chat
- File Sharing
- Emoji Support
- Notifications

---

👨‍💻 Author

- Mamun Bepari
- Aspiring Backend Developer (Python & Django)

- GitHub
https://github.com/mamun-2025