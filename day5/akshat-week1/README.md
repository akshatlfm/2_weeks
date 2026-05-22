# Full Stack Public API Explorer

This project is a simple full-stack app using:
- Backend: FastAPI (Python)
- Frontend: React + Vite

It fetches data from a public API and displays it with search functionality.

---

# 🚀 Backend Setup (FastAPI)

cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && uvicorn main:app --reload

👉 Backend runs at: http://127.0.0.1:8000  
👉 API docs: http://127.0.0.1:8000/docs

---

# 🌐 Frontend Setup (React + Vite)

cd frontend && npm install && npm run dev

👉 Frontend runs at: http://localhost:5173

---

# ⚙️ Features

- Fetches posts from FastAPI backend
- Displays data in reusable cards
- Real-time search/filter functionality
- Loading and error handling

---

# 🔗 API Used

https://jsonplaceholder.typicode.com/posts

---

# 🧠 Tech Stack

- Python (FastAPI)
- Requests + Pydantic
- React (Vite)
- JavaScript (ES6+)

---

# 📌 Notes

- Make sure backend is running before starting frontend
- If CORS error occurs, enable CORSMiddleware in FastAPI