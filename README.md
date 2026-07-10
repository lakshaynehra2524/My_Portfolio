# Lakshay's Portfolio

A personal portfolio built with **HTML** and powered by a **FastAPI** backend.

This project is more than a static portfolio—it's a portable, self-hosted professional profile that evolves over time. Instead of rebuilding or redeploying the site whenever something changes, I can update sections like achievements, projects, LinkedIn posts, and profile information through a lightweight backend.

The goal is to maintain a single place that reflects my technical journey, growth, and accomplishments while remaining easy to share, customize, and extend.

## Features

* 📄 Responsive portfolio website
* ⚡ FastAPI backend serving the frontend
* 🔗 LinkedIn post management without modifying source code
* 🖼️ Profile photo upload and replacement
* 🛠️ Interactive API documentation via FastAPI
* 🚀 Ready for deployment on platforms like Render, Railway, Fly.io, or any VPS
* 📂 Simple JSON-based storage for easy editing and portability

## Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* FastAPI
* Uvicorn

**Storage**

* JSON files

## Project Structure

```text
main.py                 FastAPI application
requirements.txt
data/
    posts.json          LinkedIn posts
    profile.json        Profile information
static/
    index.html          Portfolio website
    admin.html          Admin dashboard
    uploads/            Uploaded profile images
```

## Running Locally

```bash
pip install -r requirements.txt
export PORTFOLIO_ADMIN_KEY="your-secret-key"

uvicorn main:app --reload
```

Open:

* `/` – Portfolio
* `/admin` – Manage posts and profile
* `/docs` – Interactive API documentation

## Deployment

The application can be deployed to any platform capable of running a Python process.

Examples include:

* Render
* Railway
* Fly.io
* VPS
* Docker

Remember to configure the `PORTFOLIO_ADMIN_KEY` environment variable before deploying.

Example start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Why This Project?

Most portfolios become outdated because every update requires editing code and redeploying the website.

This project separates **presentation** from **content**, allowing me to update information through a lightweight admin interface while keeping the frontend unchanged.

Rather than acting as a one-time portfolio, it serves as a continuously evolving professional profile—a digital resume that grows alongside my experience, projects, certifications, and achievements.

## Future Improvements

* Database support
* Authentication with user accounts
* Rich markdown editor for content
* Analytics dashboard
* Blog section
* Automated deployment pipeline
* Contact form with email integration

---

Built with FastAPI as a long-term, maintainable portfolio that grows alongside my career.
