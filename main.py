import sqlite3
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def init_db():
    conn = sqlite3.connect("community.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()    

@app.get("/")
def HomePage(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/community")
def CommunityPage(request: Request):
    conn = sqlite3.connect("community.db")
    cursor = conn.cursor()
    cursor.execute("SELECT author, content FROM posts ORDER by id DESC")
    posts = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse(request, "community.html", {"request": request, "posts": posts})

@app.post("/community/post")
def CreatePost(author: str = Form(...), content: str = Form(...)):
    conn = sqlite3.connect("community.db")
    cursor = conn.cursor()
    cursor.execute("INSERT into posts (author, content) VALUES (?, ?)", (author, content))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/community", status_code=303)


@app.get("/versions")
def VersionsPage(request: Request):
    return templates.TemplateResponse(request, "versions.html", {})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)