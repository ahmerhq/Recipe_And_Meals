# 🍴 Recipe & Meals App

A simple full-stack project built with **FastAPI (backend)** and **HTML/CSS/JavaScript (frontend)**.  
It lets users sign up, log in, and explore recipes by name, category, country, or random selection.  
Users can also save a favorite meal and delete their account.

---

## ✨ Features
- Basic signup & login (no refresh tokens, no 2FA)
- Recipe search by name
- Filter recipes by category
- Get random recipe
- Get recipes by country
- Save a favorite meal
- Delete account

---

## 📡 API Endpoints

**Auth**
- `POST /signup` → Register new user  
- `POST /login` → Login  
- `DELETE /delete` → Delete account  

**Recipes**
- `POST /recipe` → Get recipe by name  
- `GET /recipe/random` → Random recipe  
- `POST /recipe/filter/{category}` → Filter by category  
- `POST /recipe/{country}` → Recipes by country  

**Favorites**
- `POST /favorite_meal` → Save favorite meal  
- `GET /recipe/favorite` → Get favorite recipe  

---

## 🛠️ Tech Stack
- **Backend:** FastAPI  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** PostgreSQL (Supabase)  
- **Deployment:** Render (backend), GitHub Pages (frontend)  

---

## ⚙️ Setup
Clone the repo:
``` git clone https://github.com/your-username/recipe-app.git```

# Backend:

`cd backend`
`pip install -r requirements.txt`
`uvicorn main:app --reload` 

Frontend:

frontend/index.html in your browser.

Notes
- Email verification is basic (any email works).

- OTP/2FA not implemented — this is just a hobby project.


Uselss Notes
- Just adding to see whether new name and email are synced with vs code or not.

