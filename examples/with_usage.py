from looptick import LoopTick
import time

with LoopTick() as looptick:
    for i in range(5):
        diff = looptick.tick()
        print(f"第 {i} 次循环耗时: {diff * looptick.NS2MS:.6f} ms")
        time.sleep(0.01)