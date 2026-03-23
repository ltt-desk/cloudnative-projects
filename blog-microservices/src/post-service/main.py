"""
Post Service - 文章服务
基于 FastAPI 的博客文章管理
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import os
import redis
import json

app = FastAPI(
    title="Post Service",
    description="Blog Post Management API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis cache
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

# In-memory storage (replace with database in production)
posts_db = {}
post_id_counter = 1

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int
    tags: Optional[List[str]] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class Post(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    view_count: int = 0

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        redis_client.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"
    
    return {
        "status": "healthy",
        "service": "post-service",
        "redis": redis_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics"""
    return {
        "posts_total": len(posts_db),
        "service": "post-service"
    }

@app.post("/api/v1/posts", response_model=Post)
async def create_post(post: PostCreate):
    """创建文章"""
    global post_id_counter
    
    new_post = Post(
        id=post_id_counter,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        tags=post.tags or [],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        view_count=0
    )
    
    posts_db[new_post.id] = new_post
    post_id_counter += 1
    
    # Cache the post
    redis_client.setex(
        f"post:{new_post.id}",
        300,  # 5 minutes cache
        json.dumps(new_post.dict(default=str))
    )
    
    return new_post

@app.get("/api/v1/posts", response_model=List[Post])
async def list_posts(
    page: int = 1,
    page_size: int = 10,
    tag: Optional[str] = None
):
    """获取文章列表"""
    posts = list(posts_db.values())
    
    if tag:
        posts = [p for p in posts if tag in p.tags]
    
    # Sort by created_at descending
    posts.sort(key=lambda x: x.created_at, reverse=True)
    
    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    
    return posts[start:end]

@app.get("/api/v1/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    """获取单篇文章"""
    # Try cache first
    cached = redis_client.get(f"post:{post_id}")
    if cached:
        post_data = json.loads(cached)
        post = Post(**post_data)
        post.view_count += 1
        return post
    
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post = posts_db[post_id]
    post.view_count += 1
    
    # Update cache
    redis_client.setex(
        f"post:{post_id}",
        300,
        json.dumps(post.dict(default=str))
    )
    
    return post

@app.put("/api/v1/posts/{post_id}", response_model=Post)
async def update_post(post_id: int, post_update: PostUpdate):
    """更新文章"""
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post = posts_db[post_id]
    
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    if post_update.tags is not None:
        post.tags = post_update.tags
    
    post.updated_at = datetime.now()
    
    # Invalidate cache
    redis_client.delete(f"post:{post_id}")
    
    return post

@app.delete("/api/v1/posts/{post_id}")
async def delete_post(post_id: int):
    """删除文章"""
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    
    del posts_db[post_id]
    redis_client.delete(f"post:{post_id}")
    
    return {"message": "Post deleted successfully"}

@app.get("/api/v1/posts/author/{author_id}", response_model=List[Post])
async def get_posts_by_author(author_id: int):
    """获取作者的所有文章"""
    posts = [p for p in posts_db.values() if p.author_id == author_id]
    posts.sort(key=lambda x: x.created_at, reverse=True)
    return posts

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
