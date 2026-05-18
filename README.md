# DevTrack Backend API

## Overview
DevTrack is a minimal Django backend API for tracking engineering issues.  
It allows users to create reporters, create issues, assign priorities, track statuses, and retrieve issue data using REST-style endpoints.

---

## How to Run

```bash
git clone https://github.com/YOUR_USERNAME/devtrack-backend.git
cd devtrack-backend
python3 -m virtualenv venv
source venv/bin/activate
pip install django
python manage.py migrate
python manage.py runserver


Server URL:
http://127.0.0.1:8000/

API Endpoints
Reporter Endpoints
POST /api/reporters/ → Create a reporter
GET /api/reporters/ → Get all reporters
GET /api/reporters/?id=1 → Get reporter by ID

Issue Endpoints
POST /api/issues/ → Create an issue
GET /api/issues/ → Get all issues
GET /api/issues/?id=1 → Get issue by ID
GET /api/issues/?status=open → Filter issues by status

Design Decision

I used an abstract BaseEntity class for both Reporter and Issue.

Why:
This allowed shared methods like validate() and to_dict() to be reused across multiple classes, reducing code duplication and improving maintainability through OOP principles.



Project Structure
DevTrack/
├── manage.py
├── reporters.json
├── issues.json
├── README.md
├── screenshots/
│   ├── success.png
│   └── failure.png
├── DevTrack/
│   ├── settings.py
│   └── urls.py
└── issues/
    ├── models.py
    ├── views.py
    └── urls.py


Author
Keerthan Salian