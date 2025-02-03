import os

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# -- 環境変数からDB接続URLを取得 (docker-compose.yml の設定を利用) --
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/todos"
)

# -- SQLAlchemyの準備 --
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    taskid = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    details = Column(Text, nullable=True)


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# テーブルが存在しない場合は作成 (本番運用ではマイグレーションツール推奨)
Base.metadata.create_all(bind=engine)

# -- FastAPIアプリケーション作成 --
app = FastAPI()


# -- Pydanticスキーマ --
class TaskCreate(BaseModel):
    name: str
    details: Optional[str] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    details: Optional[str] = None


class TaskResponse(BaseModel):
    taskid: int
    name: str
    details: Optional[str]

    class Config:
        orm_mode = True


# -- DBセッションを取得するためのDepend--
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# タスクを作成(POST)
# -------------------------
@app.post("/task", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(name=task.name, details=task.details)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# -------------------------
# タスク一覧を取得(GET)
# -------------------------
@app.get("/task", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


# -------------------------
# 特定のタスク取得(GET)
# -------------------------
@app.get("/task/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.taskid == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# -------------------------
# タスクの更新(PUT)
# -------------------------
@app.put("/task/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.taskid == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data.name is not None:
        task.name = task_data.name
    if task_data.details is not None:
        task.details = task_data.details

    db.commit()
    db.refresh(task)
    return task


# -------------------------
# タスクの削除(DELETE)
# -------------------------
@app.delete("/task/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.taskid == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"detail": f"Task {task_id} deleted successfully"}
