from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore

app = FastAPI(title="Tasks CRUD API Ighor")


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    done: bool = False


    class TaskUpdate(BaseModel):
        title: str | None = None
        description: str | None = None
        done: bool | None = None


class Task(TaskCreate):
    id: int


tasks: dict[int, Task] = {}
next_id = 1


@app.get("/")
def health_check():
    return {"message": "API de tasks online"}


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return list(tasks.values())


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    global next_id

    task = Task(id=next_id, **payload.model_dump())
    tasks[next_id] = task
    next_id += 1
    return task


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskCreate):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    
    data = task.model_dump()
    updates = payload.model_dump(exclude_unset=True)
    data.update(updates)

    updated_task = Task(**data)
    tasks[task_id] = updated_task
    return updated_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task não encontrada")
    
    del tasks[task_id]