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

