from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel,Field

app = FastAPI()

# ---------- 1. 数据模型（Pydantic）----------
class TodoCreate(BaseModel):
    #标题： 必填、非空、最长100字
    title : str = Field(min_length = 1)
    #完成状态，默认未完成
    done : bool = False

class Todo(TodoCreate):
    #继承上面两个字段，再加id
    id : int

# ---------- 2. 内存存储（暂用列表，重启会清空）----------
todos : list[Todo] = []
next_id = 1

# -----------3. 接口（REST 增删改查）-------------
#查全部
@app.get("/todos",response_model = list[Todo])
def list_todos(skip: int = Query(0,ge=0) ,limit: int = Query(10,ge=1,le=100), q : str | None = None):
    result = todos
    if q:
        result = [t for t in result if q in t.title]
    return result[skip: skip+limit]

#新增
@app.post("/todos",response_model = Todo,status_code = 201)
def create_todo(item: TodoCreate):
    global next_id
    todo = Todo(id = next_id, **item.model_dump())
    todos.append(todo)
    next_id += 1
    return todo

#查单条
@app.get("/todos/{todo_id}",response_model = Todo)
def get_todo(todo_id : int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404,detail="待办不存在")

#修改
@app.put("/todos/{todo_id}",response_model = Todo)
def update_todo(todo_id : int ,item : TodoCreate):
    for todo in todos:
        if todo.id == todo_id:
            todo.title = item.title
            todo.done = item.done
            return todo
    raise HTTPException(status_code = 404 ,detail="待办不存在")

#删除
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id : int):
    for i,todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return
    raise HTTPException(status_code=404,detail="待办不存在")
