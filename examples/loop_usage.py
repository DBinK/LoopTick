import time
from looptick import LoopTick

def prosess():
    time.sleep(0.001)  # 模拟耗时操作

loop = LoopTick()

while True:
    
    prosess()
    
    ns = loop.tick()
    hz = loop.get_hz()
    avg_hz = loop.get_avg_hz()
    
    print(f"{hz:.2f} Hz, {avg_hz:.2f} Hz, {ns * LoopTick.NS2MS:.2f} ms")