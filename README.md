# LoopTick

一个简单的 Python 循环耗时测量工具。

## Why LoopTick?

直观对比传统写法:

```python
import time
from looptick import LoopTick

def work():
    """模拟工作负载"""
    time.sleep(0.001)

## 手动计时方式
print("=== 手动计时 ===")
start_total = time.time()
times = []

for i in range(5):
    start = time.time()
    work()
    elapsed = time.time() - start
    times.append(elapsed)
    hz = 1 / elapsed if elapsed > 0 else 0
    
    # 计算实时平均Hz
    avg_elapsed = sum(times) / len(times)
    avg_hz = 1 / avg_elapsed if avg_elapsed > 0 else 0
    
    print(f"第{i+1}次: {(elapsed * 1000):.2f}ms, {hz:.2f}Hz, 平均Hz: {avg_hz:.2f}")

total_manual = (time.time() - start_total) * 1000
avg_manual = (sum(times) / len(times)) * 1000
avg_hz_manual = 1 / (sum(times) / len(times))
print(f"总耗时: {total_manual:.2f}ms, 平均: {avg_manual:.2f}ms, 平均Hz: {avg_hz_manual:.2f}Hz\n")
```

使用 LoopTick 简化此类代码的编写

```python
## 使用LoopTick
print("=== 使用LoopTick ===")
loop = LoopTick()

for i in range(5):
    diff = loop.tick()          # 获取上一次调用 tick() 的用时 (ns), 第一次调用 tick() 返回一个极小值 (0.001, 可手动设置),
    work()                      # 模拟工作负载
    hz = loop.get_hz()          # 获取当前帧率 (Hz), 第一次调用 tick() 返回的是预设值 1
    avg_hz = loop.get_avg_hz()  # 获取实时平均帧率 (Hz), 第第一次调用 tick() 默认返回 1
    print(f"第{i+1}次: {diff * loop.NS2MS:.2f}ms, {hz:.2f}Hz, 平均Hz: {avg_hz:.2f}")

print(f"总耗时: {loop.total_ms:.2f}ms, 平均: {loop.avg_ms:.2f}ms, 平均Hz: {loop.get_avg_hz():.2f}Hz\n")
```

输出结果示例：
```bash
(LoopTick) PS C:\IT\LoopTick> & C:\IT\LoopTick\.venv\Scripts\python.exe c:/IT/LoopTick/examples/with_usage.py  
=== 手动计时 ===
第1次: 1.06ms, 944.45Hz, 平均Hz: 944.45
第2次: 1.06ms, 947.87Hz, 平均Hz: 946.15
第3次: 1.05ms, 948.94Hz, 平均Hz: 947.08
第4次: 1.05ms, 950.01Hz, 平均Hz: 947.81
第5次: 1.11ms, 900.26Hz, 平均Hz: 937.90
总耗时: 5.38ms, 平均: 1.07ms, 平均Hz: 937.90Hz

=== 使用LoopTick ===
第1次: 0.00ms, 0.00Hz, 平均Hz: 100000000000.00
第2次: 1.07ms, 937.33Hz, 平均Hz: 937.33
第3次: 1.06ms, 944.60Hz, 平均Hz: 940.95
第4次: 1.06ms, 947.34Hz, 平均Hz: 943.07
第5次: 1.09ms, 917.11Hz, 平均Hz: 936.44
总耗时: 4.27ms, 平均: 1.07ms, 平均Hz: 936.44Hz
```


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
- `tick()` 在第一次调用时, 并没有 "上一次调用", 所以不能获取真正的用时, 默认返回一个极小值 (0.001, 可手动设置), `hz` 与 `avg_hz` 默认返回 1 Hz