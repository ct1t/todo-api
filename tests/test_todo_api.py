"""
Day 1 验证：用 TestClient 跑通 todo API 的增删改查
跑：uv run python tests/test_todo_api.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def main() -> None:
    # 1. 初始列表应为空
    r = client.get("/todos")
    assert r.status_code == 200, r.text
    assert r.json() == [], f"初始应为空，实际 {r.json()}"
    print("[1] GET /todos 空列表 OK")

    # 2. 新增一条
    r = client.post("/todos", json={"title": "学 FastAPI"})
    assert r.status_code == 201, r.text
    todo = r.json()
    assert todo["id"] == 1 and todo["title"] == "学 FastAPI" and todo["done"] is False
    print(f"[2] POST /todos OK -> {todo}")

    # 3. 再新增一条
    r = client.post("/todos", json={"title": "学 Pydantic", "done": True})
    assert r.status_code == 201
    print(f"[3] POST /todos OK -> {r.json()}")

    # 4. 查全部
    r = client.get("/todos")
    assert len(r.json()) == 2
    print(f"[4] GET /todos 共 {len(r.json())} 条 OK")

    # 5. 查单条
    r = client.get("/todos/1")
    assert r.status_code == 200 and r.json()["title"] == "学 FastAPI"
    print(f"[5] GET /todos/1 OK -> {r.json()}")

    # 6. 查不存在 -> 404
    r = client.get("/todos/999")
    assert r.status_code == 404
    print(f"[6] GET /todos/999 -> 404 OK")

    # 7. 修改
    r = client.put("/todos/1", json={"title": "学完 FastAPI", "done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True
    print(f"[7] PUT /todos/1 OK -> {r.json()}")

    # 8. 校验失败：title 为空 -> 422
    r = client.post("/todos", json={"title": ""})
    assert r.status_code == 422, r.text
    print(f"[8] POST /todos 空标题 -> 422 OK")

    # 9. 删除
    r = client.delete("/todos/1")
    assert r.status_code == 204
    print(f"[9] DELETE /todos/1 -> 204 OK")

    # 10. 删除后再查 -> 404
    r = client.get("/todos/1")
    assert r.status_code == 404
    print(f"[10] GET /todos/1 after delete -> 404 OK")

    print("\n✅ 全部 10 项测试通过")


if __name__ == "__main__":
    main()
