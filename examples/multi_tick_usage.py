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
print(f"looptick 测量的每次循环平均耗时: {looptick.avg_ms:.6f} ms")

# 注意: looptick 对象会少一次循环的计时, 因为在第一次调用时只能返回一个极小值 (0.000_001) 