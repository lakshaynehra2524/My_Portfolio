"""
Lakshay Portfolio — FastAPI backend.

Serves the static portfolio site and two tiny data endpoints:
  - /api/posts    a small JSON store of LinkedIn post links you add yourself
  - /api/profile  your profile photo, uploaded once via /admin

"""

import json
import os
import shutil
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = STATIC_DIR / "uploads"
POSTS_FILE = DATA_DIR / "posts.json"
PROFILE_FILE = DATA_DIR / "profile.json"
REPOS_FILE = DATA_DIR / "repos.json"

DATA_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# # Set a real secret before deploying: `export PORTFOLIO_ADMIN_KEY="something-long"`
# My secret admit key 
from admin_key.admin_key import ADMIN_KEY

app = FastAPI(title="Lakshay Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Post(BaseModel):
    title: str
    url: str
    date: str
    snippet: str = ""


class Repo(BaseModel):
    name: str
    url: str
    description: str = ""
    status: str = "active"     # "active" | "paused" | "completed"
    progress: int = 0          # 0-100, shown as a bar when status == "active"
    tags: list[str] = []
    updated: str = ""


def _load_json(path: Path, default):
    if not path.exists():
        return default
    with open(path, "r") as f:
        return json.load(f)


def _save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def check_admin(x_admin_key: Optional[str]):
    if not x_admin_key or x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-Admin-Key header")


# ---------- posts ----------

@app.get("/api/posts")
def get_posts():
    return _load_json(POSTS_FILE, [])


@app.post("/api/posts")
def add_post(post: Post, x_admin_key: Optional[str] = Header(None)):
    check_admin(x_admin_key)
    posts = _load_json(POSTS_FILE, [])
    posts.insert(0, post.dict())
    _save_json(POSTS_FILE, posts)
    return {"status": "ok", "count": len(posts)}


@app.delete("/api/posts/{index}")
def delete_post(index: int, x_admin_key: Optional[str] = Header(None)):
    check_admin(x_admin_key)
    posts = _load_json(POSTS_FILE, [])
    if index < 0 or index >= len(posts):
        raise HTTPException(status_code=404, detail="Post not found")
    removed = posts.pop(index)
    _save_json(POSTS_FILE, posts)
    return {"status": "ok", "removed": removed}


# ---------- github repos ----------

@app.get("/api/repos")
def get_repos():
    return _load_json(REPOS_FILE, [])


@app.post("/api/repos")
def add_repo(repo: Repo, x_admin_key: Optional[str] = Header(None)):
    check_admin(x_admin_key)
    repos = _load_json(REPOS_FILE, [])
    repos.insert(0, repo.dict())
    _save_json(REPOS_FILE, repos)
    return {"status": "ok", "count": len(repos)}


@app.put("/api/repos/{index}")
def update_repo(index: int, repo: Repo, x_admin_key: Optional[str] = Header(None)):
    check_admin(x_admin_key)
    repos = _load_json(REPOS_FILE, [])
    if index < 0 or index >= len(repos):
        raise HTTPException(status_code=404, detail="Repo not found")
    repos[index] = repo.dict()
    _save_json(REPOS_FILE, repos)
    return {"status": "ok", "updated": repos[index]}


@app.delete("/api/repos/{index}")
def delete_repo(index: int, x_admin_key: Optional[str] = Header(None)):
    check_admin(x_admin_key)
    repos = _load_json(REPOS_FILE, [])
    if index < 0 or index >= len(repos):
        raise HTTPException(status_code=404, detail="Repo not found")
    removed = repos.pop(index)
    _save_json(REPOS_FILE, repos)
    return {"status": "ok", "removed": removed}


# ---------- profile photo ----------

@app.get("/api/profile")
def get_profile():
    return _load_json(PROFILE_FILE, {"photo_url": None})


@app.post("/api/profile/photo")
async def upload_photo(file: UploadFile = File(...), x_admin_key: Optional[str] = Header(None)):
    check_admin(x_admin_key)
    ext = Path(file.filename).suffix.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(status_code=400, detail="Use a jpg, png, or webp file")
    dest = UPLOADS_DIR / f"profile{ext}"
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    photo_url = f"/static/uploads/{dest.name}"
    profile = _load_json(PROFILE_FILE, {})
    profile["photo_url"] = photo_url
    _save_json(PROFILE_FILE, profile)
    return {"status": "ok", "photo_url": photo_url}


# ---------- static site ----------

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/admin")
def admin():
    return FileResponse(STATIC_DIR / "admin.html")
