from looptick import LoopTick
import time

looptick = LoopTick()

# 常规调用方法
for i in range(5):
    diff = looptick.tick()
    print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
    time.sleep(0.01)
    
print(f"总耗时: {looptick.total_sec:.6f} 秒")
print(f"平均耗时: {looptick.avg_ms:.6f} ms")

# 或者用更精简的语法
for i in range(5):
    diff = looptick()  # 直接调用 __call__() 方法, 免去书写 tick()
    print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
    time.sleep(0.01)
    
print(f"总耗时: {looptick.total_sec:.6f} 秒")
print(f"平均耗时: {looptick.avg_ms:.6f} ms")