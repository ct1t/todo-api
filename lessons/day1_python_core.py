"""
Day 1 练习：Python 工程化四件套
- 类型注解：main.py 里已经大量用到（list[Todo]、int、str 等）
- 异常处理：main.py 里用了 HTTPException + 全局 handler
- 生成器：yield 懒加载，省内存
- 装饰器：在函数外面包一层，加日志/计时/缓存

跑一下：uv run python lessons/day1_python_core.py
"""

from __future__ import annotations
import time
from typing import Iterator, Callable, Any


# ========== 1. 生成器（Generator）==========
def fib(n: int) -> Iterator[int]:
    """生成前 n 个斐波那契数。用 yield，不一次性占内存。"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def read_lines_large_file(path: str) -> Iterator[str]:
    """模拟逐行读大文件：不 readlines() 一次吃进内存，而是 yield 一行。"""
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


# ========== 2. 装饰器（Decorator）==========
def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """打印函数耗时。"""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        cost = (time.perf_counter() - t0) * 1000
        print(f"  [timer] {func.__name__} 耗时 {cost:.2f} ms")
        return result
    return wrapper


def retry(times: int = 2) -> Callable:
    """带参数的装饰器：失败自动重试 times 次。"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Exception | None = None
            for i in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"  [retry] {func.__name__} 第 {i} 次失败: {e}")
            assert last_exc is not None
            raise last_exc
        return wrapper
    return decorator


# ========== 3. 类型注解 + 异常处理 综合示例 ==========
class TodoStore:
    def __init__(self) -> None:
        self._data: dict[int, str] = {}
        self._next: int = 1

    def add(self, title: str) -> int:
        if not title.strip():
            raise ValueError("标题不能为空")
        self._data[self._next] = title
        self._next += 1
        return self._next - 1

    def get(self, todo_id: int) -> str:
        if todo_id not in self._data:
            raise KeyError(f"todo {todo_id} 不存在")
        return self._data[todo_id]


@timer
@retry(times=3)
def demo_add(store: TodoStore, title: str) -> int:
    return store.add(title)


# ========== 跑一下 ==========
if __name__ == "__main__":
    print("=== 生成器：前 10 个斐波那契 ===")
    print(list(fib(10)))

    print("\n=== 装饰器：timer + retry ===")
    store = TodoStore()
    tid = demo_add(store, "学完 FastAPI")
    print(f"  add -> id={tid}, title={store.get(tid)}")

    print("\n=== 异常处理：KeyError ===")
    try:
        store.get(999)
    except KeyError as e:
        print(f"  捕获到: {e}")

    print("\n✅ Day1 练习跑完")
