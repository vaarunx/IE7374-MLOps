from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

import uvicorn

app = FastAPI()

# In-memory storage for demo purposes
tasks = {}
task_id_counter = 1


class Task(BaseModel):
    title: str
    description: str
    completed: bool = False


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


@app.get("/")
def read_root():
    return {"message": "Welcome to the Task API"}


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: Task):
    global task_id_counter
    task_id = task_id_counter
    tasks[task_id] = task.dict()
    task_id_counter += 1
    return {"id": task_id, **tasks[task_id]}


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    return [{"id": tid, **task} for tid, task in tasks.items()]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task_id, **tasks[task_id]}


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task.dict()
    return {"id": task_id, **tasks[task_id]}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)