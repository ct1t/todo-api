from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Todo API", version="0.2.0")


# ---------- 1. 数据模型（Pydantic）----------
class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="标题，非空，最长100字")
    done: bool = False


class Todo(TodoCreate):
    id: int


# ---------- 2. 内存存储（重启清空）----------
todos: list[Todo] = []
next_id: int = 1


# -----------3. 接口（REST 增删改查，全 async）-------------
@app.get("/todos", response_model=list[Todo])
async def list_todos():
    return todos


@app.post("/todos", response_model=Todo, status_code=201)
async def create_todo(item: TodoCreate):
    global next_id
    todo = Todo(id=next_id, **item.model_dump())
    todos.append(todo)
    next_id += 1
    return todo


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="待办不存在")


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, item: TodoCreate):
    for todo in todos:
        if todo.id == todo_id:
            todo.title = item.title
            todo.done = item.done
            return todo
    raise HTTPException(status_code=404, detail="待办不存在")


@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return  # 204 No Content：不返回任何 body
    raise HTTPException(status_code=404, detail="待办不存在")


# ---------- 4. 全局异常处理：未捕获异常统一返回 500 JSON ----------
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"服务器内部错误: {type(exc).__name__}"},
    )
