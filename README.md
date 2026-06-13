# HabitFlow ⚡

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-habitflow--w64i.onrender.com-e63946?style=for-the-badge)](https://habitflow-w64i.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)

![HabitFlow Banner](https://via.placeholder.com/1200x400/1e0505/e63946?text=HabitFlow+-+Premium+Habit+Tracker)

HabitFlow is a premium, high-performance habit tracking web application built with Python and Django. It abandons traditional spreadsheet-like interfaces in favor of a stunning, game-like, cyberpunk/samurai aesthetic. It focuses strictly on consistency (Streaks) rather than complex percentages, motivating users to "never break the chain."

## 🌟 Key Features

* **Smart Auto-Generation:** Automatically creates a personalized "Drink Water" habit upon registration, calculating the exact physiological daily norm (in liters) based on the user's weight.
* **Streak-Based Analytics:** The dashboard tracks and visualizes "days in a row" (🔥) to build psychological momentum. Includes a custom CSS-only vertical bar chart for weekly activity.
* **Premium Glassmorphism UI:** Built completely without bulky frontend frameworks (like Tailwind or Bootstrap). Utilizes pure CSS3 for a stunning visual experience: translucent cards, animated background gradients, glowing orbs, and Apple VisionOS-style pill buttons with inset shadows.
* **Lightning Fast:** Zero N+1 query problems. The application leverages advanced Django ORM techniques (`select_related`, `prefetch_related`, `Count`, `Q` objects) to ensure instant page loads, pushing heavy calculations to the database level.
* **Secure & Isolated:** Custom user models, strict database constraints (`unique_together` to prevent duplicate daily check-ins), and robust decorator-based authorization ensure that your habits remain completely private.

## 🛠 Tech Stack

* **Backend:** Python 3, Django 4.2+, Django ORM, SQLite / PostgreSQL
* **Frontend:** HTML5, CSS3 (Glassmorphism, Animations), Vanilla JavaScript
* **Architecture:** MVT (Model-View-Template), Service Layer Pattern, Event-Driven (Django Signals)
* **Deployment Ready:** Configured with WhiteNoise for static files and `dj-database-url` for environment-based database configuration.

## 🚀 Quick Start (Local Setup)

To get this project up and running locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/habit_tracker.git
   cd habit_tracker
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   # Optional: DATABASE_URL for Postgres
   ```

4. **Run migrations and start the server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000` in your browser.

## 📸 Screenshots

*(Replace these placeholders with actual screenshots of your app)*

| Dashboard | Analytics | Profile |
|-----------|-----------|---------|
| ![Dashboard](https://via.placeholder.com/400x300/1e0505/ffffff?text=Dashboard+View) | ![Analytics](https://via.placeholder.com/400x300/1e0505/ffffff?text=Analytics+View) | ![Profile](https://via.placeholder.com/400x300/1e0505/ffffff?text=Profile+View) |

---
*Built with ❤️ to build better versions of ourselves.*
