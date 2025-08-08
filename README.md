# LoopTick

一个简单的 Python 循环耗时测量工具。

## 安装
```bash
pip install looptick
```
本地安装
```bash
git clone https://github.com/DBinK/LoopTick
pip install -e .
```

## 使用示例
```python
from looptick import LoopTick
import time

with LoopTick() as timer:
    for i in range(5):
        diff = timer.tick()
        print(f"第 {i} 次循环耗时: {diff * timer.NS2MS:.6f} ms")
        time.sleep(0.01)
```


