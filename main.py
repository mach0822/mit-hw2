from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import time

app = FastAPI(title="AI Agent Bulletin Board API")

# In-memory storage
posts = []
post_id_counter = 1


class PostCreate(BaseModel):
    author: str
    title: str
    content: str


class Post(BaseModel):
    id: int
    author: str
    title: str
    content: str
    timestamp: float


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.get("/api/posts")
async def get_posts():
    """Get all posts sorted by newest first."""
    return {"posts": sorted(posts, key=lambda x: x["timestamp"], reverse=True)}


@app.get("/api/posts/{post_id}")
async def get_post(post_id: int):
    """Get a single post by ID."""
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@app.post("/api/posts", status_code=201)
async def create_post(post: PostCreate):
    """Create a new post."""
    global post_id_counter
    new_post = {
        "id": post_id_counter,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "timestamp": time.time()
    }
    posts.append(new_post)
    post_id_counter += 1
    return new_post


@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: int):
    """Delete a post by ID."""
    for i, post in enumerate(posts):
        if post["id"] == post_id:
            deleted = posts.pop(i)
            return {"message": "Post deleted", "post": deleted}
    raise HTTPException(status_code=404, detail="Post not found")


@app.get("/api/health")
async def health():
    return {"status": "ok", "total_posts": len(posts)}
