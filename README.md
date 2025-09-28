English Flashcards Web App with Django 📚

A simple web application for learning English vocabulary through flashcards, built with Django.

📂 Project Structure
English-Flashcards-Web-App-with-Django/
├── btlpython/        # Django project settings, urls, wsgi/asgi
├── flashcards/       # Core Django app: models, views, templates
├── media/images/     # Uploaded images for flashcards
├── mystaticfiles/    # Static assets (CSS, JS, images)
├── productionfiles/  # Deployment-related configs (optional)
├── manage.py         # Django management script
├── .gitignore

✨ Features

Add, edit, delete flashcards.

Group flashcards by topics.

Support for images in cards.

Simple UI with static files (HTML/CSS/JS).

Extendable roadmap: practice modes, spaced repetition, progress tracking.

⚙️ Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS, JavaScript

Database: SQLite (default, can switch to Postgres/MySQL)

Media/Static: Django static & media file handling

🚀 Getting Started
1. Clone the repository
git clone https://github.com/slhomles/English-Flashcards-Web-App-with-Django.git
cd English-Flashcards-Web-App-with-Django

2. Setup virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

pip install django

3. Run migrations & create superuser
python manage.py migrate
python manage.py createsuperuser

4. Start the development server
python manage.py runserver


Access at: http://127.0.0.1:8000

🗺️ Roadmap

 Multiple practice modes (MCQ, typing test).

 Spaced repetition learning.

 Progress dashboard & statistics.

 Import/export flashcards (CSV/Excel).

 REST API (Django REST Framework).

 Docker deployment.

🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📜 License

This project is licensed under the MIT License – see the LICENSE
 file for details.
