from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

# Veritabanı ayarları
DATABASE_URL = "sqlite:///./test.db"  # SQLite veritabanı
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Şifreleme için passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Uygulama tanımı
app = FastAPI()

# CORS middleware'i ekleyin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statik dosyaları servis et
app.mount("/static", StaticFiles(directory="static"), name="static")

# Kullanıcı modeli
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    email: str
    password: str

# Görev modeli
class TodoItem(BaseModel):
    id: int
    title: str
    completed: bool = False
    priority: str = "low"
    deadline: str = None

todo_list = []
archived_todo_list = []

# Veritabanını oluştur
Base.metadata.create_all(bind=engine)

# Ana sayfa (index.html)
@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("templates/index.html") as f:
        return f.read()

# Kullanıcı kaydı
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(SessionLocal)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Giriş endpoint'i
@app.post("/login")
def login(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

# Görevleri getir
@app.get("/todos")
def get_todos():
    return todo_list

# Yeni görev ekle
@app.post("/todos")
def add_todo(item: TodoItem):
    todo_list.append(item)
    return item

# Görev sil
@app.delete("/todos/{item_id}")
def delete_todo(item_id: int):
    global todo_list
    todo_list = [item for item in todo_list if item.id != item_id]
    return {"message": "Item deleted"}

# Görev güncelle
@app.put("/todos/{item_id}")
def update_todo(item_id: int, updated_item: TodoItem):
    for item in todo_list:
        if item.id == item_id:
            item.title = updated_item.title
            item.completed = updated_item.completed
            item.priority = updated_item.priority
            item.deadline = updated_item.deadline
            return {"message": "Item updated"}
    return {"error": "Item not found"}

# Görevin tamamlanma durumu değiştir
@app.put("/todos/{item_id}/complete")
def complete_todo(item_id: int):
    for item in todo_list:
        if item.id == item_id:
            item.completed = not item.completed
            return {"message": "Item completion toggled"}
    return {"error": "Item not found"}

# Görevleri filtrele (tamamlanmış veya tamamlanmamış)
@app.get("/todos/filter")
def filter_todos(completed: bool):
    return [item for item in todo_list if item.completed == completed]

# Görevleri sıralama (tarih veya başlığa göre)
@app.get("/todos/sort")
def sort_todos(by: str):
    if by == "date":
        return sorted(todo_list, key=lambda x: x.id)
    elif by == "title":
        return sorted(todo_list, key=lambda x: x.title)
    return {"error": "Invalid sort parameter"}

# Görevleri önceliğe göre filtreleme
@app.get("/todos/priority")
def get_priority_todos(priority: str):
    return [item for item in todo_list if item.priority == priority]

# Tarihi yaklaşan görevler
@app.get("/todos/upcoming")
def get_upcoming_todos():
    upcoming_tasks = []
    for item in todo_list:
        if item.deadline:
            task_date = datetime.strptime(item.deadline, "%Y-%m-%d")
            if task_date > datetime.now():
                upcoming_tasks.append(item)
    return upcoming_tasks

# Görevleri arşivleme
@app.post("/todos/{item_id}/archive")
def archive_todo(item_id: int):
    global todo_list
    for item in todo_list:
        if item.id == item_id:
            archived_todo_list.append(item)
            todo_list = [t for t in todo_list if t.id != item_id]
            return {"message": "Item archived"}
    return {"error": "Item not found"}

# Arşivlenmiş görevleri getir
@app.get("/todos/archived")
def get_archived_todos():
    return archived_todo_list

# Ana sayfa (index.html)
@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("templates/index.html") as f:
        return f.read()

# Kayıt sayfası (register.html)
@app.get("/register", response_class=HTMLResponse)
def serve_register():
    with open("templates/register.html") as f:
        return f.read()

# Giriş sayfası (login.html)
@app.get("/login", response_class=HTMLResponse)
def serve_login():
    with open("templates/login.html") as f:
        return f.read()
