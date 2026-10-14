from fastapi import FastAPI,HTTPException,Query,Request
from pydantic import BaseModel,Field
from fastapi.responses import JSONResponse

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

class TodoUpdate(BaseModel):
    title : str | None = None
    done : bool = False

# ---------- 2. 内存存储（暂用列表，重启会清空）----------
todos : list[Todo] = []
next_id = 1

# -----------3. 接口（REST 增删改查）-------------
#查全部
@app.get("/todos",response_model = list[Todo])
async def list_todos(skip: int = Query(0,ge=0) ,
                     limit: int = Query(10,ge=1,le=100), 
                     q : str | None = None,
                     done : bool | None = None,
                     ):
    result = todos
    if q:
        result = [t for t in result if q in t.title]
    if done is not None:
        result = [t for t in result if t.done == done]
    return result[skip: skip+limit]

#新增
@app.post("/todos",response_model = Todo,status_code = 201)
async def create_todo(item: TodoCreate):
    global next_id
    todo = Todo(id = next_id, **item.model_dump())
    todos.append(todo)
    next_id += 1
    return todo

#查单条
@app.get("/todos/{todo_id}",response_model = Todo)
async def get_todo(todo_id : int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404,detail="待办不存在")

#修改
@app.put("/todos/{todo_id}",response_model = Todo)
async def update_todo(todo_id : int ,item : TodoCreate):
    for todo in todos:
        if todo.id == todo_id:
            todo.title = item.title
            todo.done = item.done
            return todo
    raise HTTPException(status_code = 404 ,detail="待办不存在")
#部分更新
@app.patch("/todo_id/{todo_id}",response_model=Todo)
def patch_todo(todo_id:int ,item : TodoUpdate):
    for todo in todos:
        if todo.id == todo_id:
            if item.title is not None:
                todo.title = item.title
            if item.done is not None:
                todo.done = item.done
            return todo
    raise HTTPException(status_code = 404,detail="待办不存在")

#删除
@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id : int):
    for i,todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return
    raise HTTPException(status_code=404,detail="待办不存在")

@app.exception_handler(Exception)
async def global_error_handler(request: Request,exc: Exception):
    return JSONResponse(
        status_code = 500,
        content={"detail":f"服务器出错: {type(exc).__name__}"}
    )