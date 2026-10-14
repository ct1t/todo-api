# Todo API · 待办事项接口

第 1 周（10.14–10.18）学习项目：用 FastAPI 实现的待办事项增删改查接口。

## 技术栈
FastAPI · Pydantic v2 · uvicorn · uv 管理依赖

## 启动
```bash
uv run fastapi dev main.py
```
启动后访问 http://127.0.0.1:8000/docs （自动生成的 Swagger 文档，可直接在页面上点接口测试）

## 跑测试
```bash
uv run python tests/test_todo_api.py
```

## 接口
| 方法 | 路径 | 说明 | 状态码 |
|---|---|---|---|
| GET | /todos | 查全部 | 200 |
| POST | /todos | 新增待办 | 201 / 422（校验失败）|
| GET | /todos/{id} | 查单条 | 200 / 404 |
| PUT | /todos/{id} | 修改 | 200 / 404 |
| DELETE | /todos/{id} | 删除 | 204 / 404 |

## 本周练到的知识点
- **Python**：类型注解、异常处理（HTTPException + 全局 handler）、生成器（`yield`）、装饰器（见 `lessons/day1_python_core.py`）
- **FastAPI**：路由、路径参数、Pydantic 请求体校验（自动 422）、`async def` 异步接口
- **Git**：分支/合并/PR 流程（见下方提交历史）

## 三年目标（写在 README 里）
- **研一上（现在→2027.1）**：打地基。FastAPI/RAG/Agent 入门，复现 ReAct，蓝桥杯省赛。
- **研一下（2027.2–2027.7）**：出成果。RAG/Agent 方向发 1 篇小论文，参加 1 次竞赛（Kaggle/天池）。
- **研二（2027.9–2028.6）**：定方向。深挖 LLM 应用某子方向（多模态 Agent / 垂直领域 RAG），暑假去大厂实习。
- **研三（2028.9–2029.6）**：毕业论文 + 秋招。目标岗位：大模型应用工程师 / Agent 开发。

## 说明
数据暂存内存（重启清空），后续接入数据库。
