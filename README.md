# Todo API · 待办事项接口

第 2 周（阶段1 打地基）学习项目：用 FastAPI 实现的待办事项增删改查接口。

## 技术栈
FastAPI 0.143 · Pydantic v2 · uvicorn（uv 管理依赖）

## 启动
uv run fastapi dev main.py
启动后访问 http://127.0.0.1:8000/docs

## 接口
| 方法 | 路径 | 说明 | 状态码 |
|---|---|---|---|
| GET | /todos | 查全部 | 200 |
| POST | /todos | 新增待办 | 201 |
| GET | /todos/{id} | 查单条 | 200 / 404 |
| PUT | /todos/{id} | 修改 | 200 / 404 |
| DELETE | /todos/{id} | 删除 | 204 / 404 |

## 说明
数据暂存内存（重启清空），第 12 周接入 PostgreSQL。
