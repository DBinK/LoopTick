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
常规方式测量循环用时

```python
from looptick import LoopTick
import time

looptick = LoopTick()
for i in range(5):
    diff = looptick.tick()
    print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
    time.sleep(0.01)

looptick.__exit__()
```

使用上下文方式

```python
from looptick import LoopTick
import time

with LoopTick() as looptick:
    for i in range(5):
        diff = looptick.tick()
        print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
        time.sleep(0.01)
```

输出结果示例：
```bash
(LoopTick) PS C:\IT\LoopTick> & C:\IT\LoopTick\.venv\Scripts\python.exe c:/IT/LoopTick/examples/with_usage.py  
第 0 次循环耗时: 0.000000 ms
第 1 次循环耗时: 10.829900 ms
第 2 次循环耗时: 16.055800 ms
第 3 次循环耗时: 14.013400 ms
第 4 次循环耗时: 15.587100 ms
总耗时: 0.056486 秒
平均耗时: 14.121550 ms
```


