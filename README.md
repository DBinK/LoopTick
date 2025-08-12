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

### 测量每个循环用时

常规方式

```python
from looptick import LoopTick
import time

looptick = LoopTick()

# 常规调用方式
for i in range(5):
    diff = looptick.tick()
    print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
    time.sleep(0.01)
    
print(f"总耗时: {looptick.total_sec:.6f} 秒")
print(f"平均耗时: {looptick.average_ms:.6f} ms")

# 或者用更精简的语法
for i in range(5):
    diff = looptick()  # 直接调用 __call__() 方法, 免去书写 tick()
    print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
    time.sleep(0.01)
```

使用上下文方式

```python
from looptick import LoopTick
import time

with LoopTick() as looptick:
with LoopTick() as looptick:
    for i in range(5):
        diff = looptick.tick()
        print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
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


### 测量行间代码用时
```python
from looptick import LoopTick
import time

def stage1():
    time.sleep(0.02)  # 模拟 I/O 操作

def stage2():
    time.sleep(0.05)  # 模拟复杂计算

def stage3():
    time.sleep(0.01)  # 模拟轻量处理

# 使用多阶段测量
linetick = LoopTick()

for i in range(3):  # 模拟 1000 次循环

    start = linetick.tick()  # 第一次调用, 返回一个极小值 (0.000_001) 
                             # 完成一次循环后, 返回上一次循环的 mid2 -> start 的用时
                             # 一般我们不关心 start 变量的值, 仅表示测量开始
    stage1()  
    stage2() 

    mid1 = linetick.tick()   # 返回 start —> mid1 的用时

    stage3()  

    mid2 = linetick.tick()   # 返回 mid1 —> mid2 的用时

    print(f"\n第 {i} 次循环")
    print(f"stage1() + stage2() 耗时: {mid1 * linetick.NS2MS:.2f} ms")
    print(f"stage3() 耗时: {mid2 * linetick.NS2MS:.2f} ms")
    print(f"本循环总耗时: {(mid1 + mid2) * linetick.NS2MS:.2f} ms")
    
print(f"\n循环任务总耗时: {linetick.total_sec:.6f} 秒")
```
输出结果示例：
```bash
(LoopTick) PS C:\IT\LoopTick> & C:\IT\LoopTick\.venv\Scripts\python.exe c:/IT/LoopTick/examples/lines_usage.py     

第 0 次循环
stage1() + stage2() 耗时: 93.78 ms
stage3() 耗时: 15.10 ms
本循环总耗时: 108.88 ms

第 1 次循环
stage1() + stage2() 耗时: 89.86 ms
stage3() 耗时: 15.11 ms
本循环总耗时: 104.97 ms

第 2 次循环
stage1() + stage2() 耗时: 89.71 ms
stage3() 耗时: 15.01 ms
本循环总耗时: 104.72 ms

循环任务总耗时: 0.319596 秒
```

### 进阶用法: 多 Tick 测量
```python
from looptick import LoopTick
import time

def stage1():
    time.sleep(0.02)  # 模拟 I/O 操作

def stage2():
    time.sleep(0.05)  # 模拟复杂计算

def stage3():
    time.sleep(0.03)  # 模拟轻量处理

# 使用多阶段测量 + 单独循环测量
linetick = LoopTick()
looptick = LoopTick()

for i in range(3):  # 模拟 1000 次循环

    loop_ns = looptick.tick()  # 单独使用一个对象测量循环时间

    start = linetick.tick()  # 第一次调用, 返回一个极小值 (0.000_001) 
                             # 完成一次循环后, 返回上一次循环的 mid2 -> start 的用时
                             # 一般我们不关心 start 变量的值, 仅表示测量开始
                            
    stage1()  
    stage2() 

    mid1 = linetick.tick()     # 返回 start —> mid1 的用时

    stage3()  

    mid2 = linetick.tick()     # 返回 mid1 —> mid2 的用时

    print(f"\n第 {i} 次循环")
    print(f"stage1() + stage2() 耗时: {mid1 * linetick.NS2MS:.2f} ms")
    print(f"stage3() 耗时: {mid2 * linetick.NS2MS:.2f} ms")

    print(f"linetick 对象测量的循环耗时: {(mid1 + mid2) * linetick.NS2MS:.2f} ms")
    print(f"looptick 对象测量的循环耗时: {loop_ns * linetick.NS2MS:.2f} ms")

    
print(f"\nlinetick 对象测量的循环任务总耗时: {linetick.total_sec:.6f} 秒")

print(f"looptick 对象测量的循环任务总耗时: {looptick.total_sec:.6f} 秒")  
print(f"looptick 测量的每次循环平均耗时: {looptick.average_ms:.6f} ms")

# 注意: looptick 对象会少一次循环的计时, 因为在第一次调用时只能返回一个极小值 (0.000_001) 
```

输出结果示例：
```bash
(LoopTick) PS C:\IT\LoopTick> & C:\IT\LoopTick\.venv\Scripts\python.exe c:/IT/LoopTick/examples/multi_tick_usage.py

第 0 次循环
stage1() + stage2() 耗时: 94.48 ms
stage3() 耗时: 45.04 ms
linetick 对象测量的循环耗时: 139.52 ms
looptick 对象测量的循环耗时: 0.00 ms

第 1 次循环
stage1() + stage2() 耗时: 89.68 ms
stage3() 耗时: 44.96 ms
linetick 对象测量的循环耗时: 134.65 ms
looptick 对象测量的循环耗时: 140.12 ms

第 2 次循环
stage1() + stage2() 耗时: 89.43 ms
stage3() 耗时: 44.88 ms
linetick 对象测量的循环耗时: 134.31 ms
looptick 对象测量的循环耗时: 135.23 ms

linetick 对象测量的循环任务总耗时: 0.409659 秒
looptick 对象测量的循环任务总耗时: 0.275349 秒
looptick 测量的每次循环平均耗时: 137.674650 ms
```

## 已知问题
- [] 在第一次调用时只能返回一个极小值 (0.000_001)