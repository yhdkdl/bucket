# 🪣 Bucket

> **Your Next Adventure, Powered by AI**

Bucket is an intelligent, gamified web application that builds custom scavenger hunts, dynamic itineraries, and personalized bucket lists based on your precise location and group preferences. Built with a stunning Digital Brutalism-inspired aesthetic, the app seamlessly integrates AI-generated activity tracking with beautiful memory collage generation.

---

## ✨ Features

- **AI-Powered Exploration**: Automatically generates unique, hyper-local adventures utilizing large language models.
- **Customizable Runs**: Filter generated adventures by Group Type (Solo, Couple, Friends, Family), Budget Level (Free, Budget, Splurge), and specific geographic destinations.
- **Sleek Custom Dashboard**: A robust routing dashboard tracking your `Ongoing`, `Completed`, and `Saved` adventures.
- **Gamified Progress Tracking**: Built-in checklists for each hunt with responsive progress indicator circles and linear status bars.
- **Memory Collages**: Upon completion of all tasks in an adventure, unlock a dynamic grid collage customizer to generate, preview, and download a gorgeous memory board of your journey (supports Horizontal and Vertical layouts).
- **Secure Authentication**: Encrypted JWT authentication system ensuring user history and privacy are tightly safeguarded.

---

## 🏗️ Folder Structure

The repository is built as a split-stack architecture consisting of a Python/Django backend API and a Vue 3 frontend client.

```text
bucket/
├── backend/                  # Django REST API & AI Generation Engine
│   ├── accounts/             # Custom User authentication & Token management
│   ├── buckets/              # Core application logic (Buckets, Items, Progress)
│   ├── config/               # Main Django settings & URL routing
│   ├── media/                # Uploaded task photos & cached Memory Collages
│   ├── services/             # OpenAI integrations and external API wrappers
│   ├── manage.py             # Django execution script
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # Vue 3 UI Client
│   ├── public/               # Static base assets
│   ├── src/                  
│   │   ├── components/       # Reusable UI (MainLayout, Navigation, Widgets)
│   │   ├── router/           # Vue-Router configuration maps & route guards
│   │   ├── services/         # Axios API clients for backend communication
│   │   └── views/            # Full-page compositions (Landing, Gen, Dashboard)
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite build configurations
```

---

## 💻 Tech Stack

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Tooling**: Vite
- **Routing**: Vue Router
- **Styling**: Vanilla CSS3 (Custom Design System, Functional Component Scoping)

### Backend
- **Framework**: Python / Django
- **API**: Django REST Framework (DRF)
- **AI Integration**: Standardized integration for adventure data generation.
- **Database**: Local SQLite (dev) / PostgreSQL (production-ready)
- **Authentication**: JWT via typical DRF token management strategies.

---

## 🚀 Setup & Installation Guide

### Prerequisites
- [Node.js](https://nodejs.org/) (v18+ recommended)
- [Python](https://www.python.org/downloads/) (3.10+ recommended)

### 1. Starting the Backend (Django)

```bash
# Navigate into the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install all Python dependencies
pip install -r requirements.txt

# Environment Setup
# Duplicate `.env.example` to `.env` and fill in necessary API Keys
# (e.g. your OPENAI_API_KEY)

# Run database migrations
python manage.py migrate

# Start the local development server
python manage.py runserver
```

> The API will be available locally at `http://127.0.0.1:8000/`.

### 2. Starting the Frontend (Vue/Vite)

Open a **new terminal window/tab**, leaving the backend server running.

```bash
# Navigate to the frontend directory
cd frontend

# Install necessary Node packages
npm install

# Start the Vite development server
npm run dev
```

> Your frontend client will register and be accessible in your browser at `http://localhost:5173`. Make sure the Python server is running simultaneously so the app can communicate with the backend!

---

## 🎨 Design Philosophy
Bucket implements a modern, slightly-brutalist but user-friendly interface. Characterized by high-contrast whites, deep slate shadows, crisp cyan (`#00e5ff`) call-to-actions, and dynamic rounded grid layouts. All form inputs and progress states were custom engineered to avoid native browser UI sluggishness and maximize user retention.

---

## 🗺️ Project Roadmap
- [x] Integrate Global Auth & Routing wrapper layouts.
- [x] Generator Engine UX Overhaul.
- [x] History & Dynamic Tab Dashboards.
- [x] Task Completion & Memory Collage Module.
- [ ] Social Features: Community Leaderboards & Shared Hunts.
- [ ] Mobile PWA packaging.

---
*Built with ❤️ for modern explorers.*
