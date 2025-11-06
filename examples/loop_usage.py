import time
from looptick import LoopTick

def precise_delay(duration):
    """精确延时函数"""
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
        pass

loop = LoopTick()
hz = 0
avg_hz = 0
while True:
    
    precise_delay(0.001)  # 模拟耗时操作, Windows 最快只能 0.001 秒, Linux 可以到 0.000_001 秒
    
    ns = loop.tick()
    print(f"{hz:.2f} Hz, {avg_hz:.2f} Hz, {ns } ns")
    
    hz = loop.get_hz()
    avg_hz = loop.get_avg_hz()